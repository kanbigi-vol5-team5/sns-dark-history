import Link from "next/link";

export const metadata = {
  title: "SNS | movie",
};

export default function Page() {
  return (
    <>
      <div className="h-screen flex items-center justify-center flex-col">
        <h1 className="text-3xl font-bold">黒歴史を振り返る</h1>
        <div className="items-center justify-center flex flex-col mt-12">
          <img src="/img/movie_player.png"></img>
        </div>
        <div className="items-center justify-center flex flex-col">
          <button className="mt-12 px-9 py-3 w-48 bg-black text-white rounded-full shadow-md hover:bg-red-600">
            リンクを共有する
          </button>
          <button className="mt-8 px-9 py-3 w-48 bg-black text-white rounded-full shadow-md hover:bg-red-600">
            動画を保存する
          </button>
          <Link href="/">
            <button className="mt-8 px-9 py-3 w-48 bg-black text-white rounded-full shadow-md hover:bg-red-600">
              トップに戻る
            </button>
          </Link>
        </div>
      </div>
    </>
  );
}
