"use client";

import React, { useRef, useState, useEffect } from "react";

// 落下物の型定義（good: スコア加算、bad: ライフ減少、power: シールド付与）
interface FallingObject {
  id: number;
  x: number;
  y: number;
  caught?: boolean;
  type: "good" | "bad" | "power";
  fallSpeed: number;
}

// 爆発エフェクトの型定義（power キャッチ時は "SHIELD!" と表示）
interface Explosion {
  id: number;
  x: number;
  y: number;
  text: string;
}

interface GameState {
  playerX: number;
  fallingObjects: FallingObject[];
}

export default function LoadingUI({ title, description }: Readonly<{ title: string, description: string }>) {
  const gameContainerRef = useRef<HTMLDivElement | null>(null);
  const gameStateRef = useRef<GameState>({ playerX: 50, fallingObjects: [] });
  const startTimeRef = useRef<number>(Date.now());
  const lastSpawnTimeRef = useRef<number>(Date.now());
  const lastCatchTimeRef = useRef<number>(0);

  const [tick, setTick] = useState<number>(0);
  const [score, setScore] = useState<number>(0);
  const [lives, setLives] = useState<number>(3);
  const [gameOver, setGameOver] = useState<boolean>(false);
  const [paused, setPaused] = useState<boolean>(false);
  const [highScore, setHighScore] = useState<number>(0);
  const [combo, setCombo] = useState<number>(1);
  const [explosions, setExplosions] = useState<Explosion[]>([]);
  const [isInvincible, setIsInvincible] = useState<boolean>(false);
  const [shieldEndTime, setShieldEndTime] = useState<number | null>(null);
  const [isGameStarted, setIsGameStarted] = useState(false); // ゲーム開始状態を管理

  // Audio オブジェクトの初期化（サウンドファイルは /public/sounds に配置）
  const goodSound = useRef<HTMLAudioElement | null>(null);
  const badSound = useRef<HTMLAudioElement | null>(null);
  const powerSound = useRef<HTMLAudioElement | null>(null);
  const gameOverSound = useRef<HTMLAudioElement | null>(null);

  // ヘルパー関数：サウンドをクローンして再生（重ね再生対応）
  const playSound = (audio: HTMLAudioElement | null) => {
    if (audio) {
      const clone = audio.cloneNode(true) as HTMLAudioElement;
      clone.play();
    }
  };


  console.log(tick);
  useEffect(() => {
    goodSound.current = new Audio("/sounds/good.mp3");
    badSound.current = new Audio("/sounds/bad.mp3");
    powerSound.current = new Audio("/sounds/power.mp3");
    gameOverSound.current = new Audio("/sounds/gameover.mp3");

    const storedHighScore = localStorage.getItem("highScore");
    if (storedHighScore) {
      setHighScore(parseInt(storedHighScore, 10));
    }
  }, []);

  useEffect(() => {
    if (lives <= 0) {
      setGameOver(true);
    }
  }, [lives]);

  useEffect(() => {
    if (gameOver) {
      if (score > highScore) {
        setHighScore(score);
        localStorage.setItem("highScore", score.toString());
      }
      playSound(gameOverSound.current);
    }
  }, [gameOver, score, highScore]);

  // キーボード操作（左右移動）
  const leftPressedRef = useRef<boolean>(false);
  const rightPressedRef = useRef<boolean>(false);
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowLeft") leftPressedRef.current = true;
      if (e.key === "ArrowRight") rightPressedRef.current = true;
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.key === "ArrowLeft") leftPressedRef.current = false;
      if (e.key === "ArrowRight") rightPressedRef.current = false;
    };

    window.addEventListener("keydown", handleKeyDown);
    window.addEventListener("keyup", handleKeyUp);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  // タッチ操作：タッチ位置に合わせてプレイヤーを移動
  const handleTouchMove = (e: React.TouchEvent) => {
    if (gameContainerRef.current) {
      const rect = gameContainerRef.current.getBoundingClientRect();
      const touch = e.touches[0];
      const x = touch.clientX - rect.left;
      const newPlayerX = Math.max(0, Math.min(x - 25, rect.width - 50));
      gameStateRef.current.playerX = newPlayerX;
    }
  };

  useEffect(() => {
    let animationFrameId: number;

    const gameLoop = () => {
      if (gameOver || paused) {
        animationFrameId = requestAnimationFrame(gameLoop);
        return;
      }
      const container = gameContainerRef.current;
      if (!container) {
        animationFrameId = requestAnimationFrame(gameLoop);
        return;
      }
      const containerWidth = container.clientWidth;
      const containerHeight = container.clientHeight;

      // 経過時間に応じた難易度調整（基本の落下速度と生成間隔）
      const elapsedTime = Date.now() - startTimeRef.current;
      const baseSpeed = 2 + Math.floor(elapsedTime / 10000) * 0.5;
      const dynamicSpawnInterval = Math.max(
        500,
        1000 - Math.floor(elapsedTime / 10000) * 50
      );

      let newPlayerX = gameStateRef.current.playerX;
      if (leftPressedRef.current) newPlayerX -= 5;
      if (rightPressedRef.current) newPlayerX += 5;
      newPlayerX = Math.max(0, Math.min(newPlayerX, containerWidth - 50));
      gameStateRef.current.playerX = newPlayerX;

      // 各落下物は自身の fallSpeed で下に移動
      const updatedFallingObjects = gameStateRef.current.fallingObjects.map(
        (obj) => ({
          ...obj,
          y: obj.y + obj.fallSpeed,
        })
      );

      const playerY = containerHeight - 60;
      const playerWidth = 50;
      const playerHeight = 50;
      updatedFallingObjects.forEach((obj) => {
        const objX = obj.x;
        const objY = obj.y;
        const objWidth = 30;
        const objHeight = 30;
        if (
          newPlayerX < objX + objWidth &&
          newPlayerX + playerWidth > objX &&
          playerY < objY + objHeight &&
          playerY + playerHeight > objY
        ) {
          if (!obj.caught) {
            let explosionText = "BOOM!";
            if (obj.type === "good") {
              if (Date.now() - lastCatchTimeRef.current < 2000) {
                setCombo((prev) => prev + 1);
              } else {
                setCombo(1);
              }
              lastCatchTimeRef.current = Date.now();
              setScore((prev) => prev + combo);
              playSound(goodSound.current);
            } else if (obj.type === "bad") {
              // bad 落下物：無敵状態の場合はライフ減少させない
              if (!isInvincible) {
                setLives((prev) => {
                  const newLives = prev - 1;
                  if (newLives <= 0) {
                    setGameOver(true);
                  }
                  return Math.max(0, newLives);
                });
                playSound(badSound.current);
              }
              setCombo(1);
            } else if (obj.type === "power") {
              setIsInvincible(true);
              setShieldEndTime(Date.now() + 5000);
              playSound(powerSound.current);
              explosionText = "SHIELD!";
            }
            const explosionId = Date.now();
            const explosion: Explosion = {
              id: explosionId,
              x: obj.x + 15,
              y: obj.y + 15,
              text: explosionText,
            };
            setExplosions((prev) => [...prev, explosion]);
            setTimeout(() => {
              setExplosions((prev) =>
                prev.filter((exp) => exp.id !== explosionId)
              );
            }, 500);
            obj.caught = true;
          }
        }
      });

      gameStateRef.current.fallingObjects = updatedFallingObjects.filter(
        (obj) => !obj.caught && obj.y < containerHeight
      );

      // 新しい落下物の生成
      // 確率変更：60% good, 35% bad, 5% power
      if (Date.now() - lastSpawnTimeRef.current > dynamicSpawnInterval) {
        const rand = Math.random();
        let newType: "good" | "bad" | "power";
        if (rand < 0.6) newType = "good";
        else if (rand < 0.95) newType = "bad";
        else newType = "power";

        const randomMultiplier = Math.random() * (1.2 - 0.8) + 0.8;
        const fallSpeed = baseSpeed * randomMultiplier;

        const newObj: FallingObject = {
          id: Date.now(),
          x: Math.random() * (containerWidth - 30),
          y: -30,
          type: newType,
          fallSpeed,
        };
        gameStateRef.current.fallingObjects.push(newObj);
        lastSpawnTimeRef.current = Date.now();
      }

      setTick((prev) => prev + 1);
      animationFrameId = requestAnimationFrame(gameLoop);
    };

    animationFrameId = requestAnimationFrame(gameLoop);
    return () => cancelAnimationFrame(animationFrameId);
  }, [gameOver, paused, combo, isInvincible]);

  // シールド解除タイマー
  useEffect(() => {
    if (isInvincible && shieldEndTime) {
      const timer = setInterval(() => {
        if (Date.now() >= shieldEndTime) {
          setIsInvincible(false);
          setShieldEndTime(null);
          clearInterval(timer);
        }
      }, 100);
      return () => clearInterval(timer);
    }
  }, [isInvincible, shieldEndTime]);

  const resetGame = () => {
    setScore(0);
    setLives(3);
    setCombo(1);
    setIsInvincible(false);
    setShieldEndTime(null);
    gameStateRef.current.playerX = 50;
    gameStateRef.current.fallingObjects = [];
    lastSpawnTimeRef.current = Date.now();
    startTimeRef.current = Date.now();
    setGameOver(false);
  };

  const startGame = () => {
    setIsGameStarted(true); // ゲームを開始
  };

  if (!isGameStarted) {
    // ゲーム開始前の画面
    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          backgroundColor: "#000",
          color: "#fff",
          textAlign: "center",
          overflow: "hidden",
        }}
      >
        <h1 style={{ fontSize: "2rem", marginBottom: "20px" }}>{title}</h1>
        <p style={{ marginBottom: "20px" }}>{description}</p>
        <button
          onClick={startGame}
          style={{
            padding: "10px 20px",
            backgroundColor: "#0070f3",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          ゲームを開始する
        </button>
      </div>
    );
  }

  return (
    <div
      ref={gameContainerRef}
      onTouchMove={handleTouchMove}
      style={{
        position: "relative",
        overflow: "hidden",
        width: "100vw", // ビューポート全体の幅
        height: "100vh", // ビューポート全体の高さ
        margin: "0", // 余白を削除

        border: "2px solid #000",
        backgroundImage: "url('/images/background.png')",
        backgroundSize: "cover",
        backgroundPosition: "center", // 背景画像を中央に配置
      }}
    >
      {/* スコア・コンボ表示 */}
      <div
        style={{
          position: "absolute",
          top: "40px",
          left: "10px",
          fontSize: "1.5rem",
          fontWeight: "bold",
          color: "#fff",
          textShadow: "1px 1px 2px #000",
        }}
      >
        Score: {score}
      </div>

      {/* ライフ表示 */}
      <div
        style={{
          position: "absolute",
          top: "10px",
          left: "10px",
          fontSize: "1.5rem",
          fontWeight: "bold",
          color: "#fff",
          textShadow: "1px 1px 2px #000",
        }}
      >
        Lives: {lives}
      </div>

      {/* ハイスコア表示 */}
      <div
        style={{
          position: "absolute",
          top: "70px",
          left: "10px",
          fontSize: "1.2rem",
          fontWeight: "bold",
          color: "#ff0",
          textShadow: "1px 1px 2px #000",
        }}
      >
        High Score: {highScore}
      </div>

      {/* シールド状態表示 */}
      {isInvincible && (
        <div
          style={{
            position: "absolute",
            top: "100px",
            left: "50%",
            transform: "translateX(-50%)",
            fontSize: "1.2rem",
            fontWeight: "bold",
            color: "#0f0",
            textShadow: "1px 1px 2px #000",
          }}
        >
          Shield Active!
        </div>
      )}

      {/* ポーズ／再開ボタン */}
      <button
        onClick={() => setPaused((prev) => !prev)}
        style={{
          position: "absolute",
          top: "30px",
          right: "30px",
          transform: "translateX(-50%)",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          zIndex: 10,
        }}
      >
        <img
          src={paused ? "/img/resume.png" : "/img/pause.png"}
          alt={paused ? "Resume" : "Pause"}
          style={{
            width: "40px", // 画像の幅
            height: "40px", // 画像の高さ
          }}
        />
      </button>

      {/* 落下物レンダリング */}
      {gameStateRef.current.fallingObjects.map((obj) => (
        <img
          key={obj.id}
          src={
            obj.type === "good"
              ? "/images/falling-object.png"
              : obj.type === "bad"
              ? "/images/bad-object.png"
              : "/images/power-object.png"
          }
          alt={
            obj.type === "good"
              ? "Good Object"
              : obj.type === "bad"
              ? "Bad Object"
              : "Power Object"
          }
          style={{
            position: "absolute",
            left: obj.x,
            top: obj.y,
            width: "30px",
            height: "30px",
          }}
        />
      ))}

      {/* プレイヤー表示 */}
      <img
        src="/images/player.png"
        alt="Player"
        style={{
          position: "absolute",
          left: gameStateRef.current.playerX,
          bottom: "10px",
          width: "50px",
          height: "50px",
          border: isInvincible ? "2px solid #0f0" : "none",
        }}
      />

      {/* 爆発エフェクト */}
      {explosions.map((exp) => (
        <div
          key={exp.id}
          style={{
            position: "absolute",
            left: exp.x,
            top: exp.y,
            pointerEvents: "none",
            fontSize: "20px",
            color: exp.text === "SHIELD!" ? "#0f0" : "yellow",
            textShadow: "0 0 5px red",
            animation: "explode 0.5s ease-out forwards",
          }}
        >
          {exp.text}
        </div>
      ))}

      {/* ゲームオーバーオーバーレイ */}
      {gameOver && (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0,0,0,0.5)",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            color: "#fff",
            fontSize: "2rem",
            zIndex: 20,
          }}
        >
          <div>Game Over</div>
          <button
            onClick={resetGame}
            style={{
              padding: "10px 20px",
              backgroundColor: "#0070f3",
              color: "#fff",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              marginTop: "20px",
            }}
          >
            Retry
          </button>
        </div>
      )}

      {/* キーフレーム定義 */}
      <style jsx>{`
        @keyframes explode {
          from {
            opacity: 1;
            transform: scale(1);
          }
          to {
            opacity: 0;
            transform: scale(2);
          }
        }
      `}</style>
    </div>
  );
}
