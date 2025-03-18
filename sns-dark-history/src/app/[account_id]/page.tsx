"use client";
import axios from "axios";
import useSWR from "swr";
import Link from "next/link";
import { useParams } from "next/navigation";
import LoadingUI from "../../compornent/loading";

async function fetcher(key: string) {
  return fetch(key).then((res) => res.json() as Promise<Array<string> | null>);
}

export default function Page() {
  const { account_id } = useParams();

  const { data, error, isLoading } = useSWR(
    `/api/dark_posts/${account_id}`,
    fetcher
  );
  if (error)
    return (
      <>
        <div className="h-screen flex items-center justify-center flex-col background-color-gray">
          <img src="/img/500error.jpg" alt="エラー" className="mt-4 mx-auto" />
          <div className="font-bold text-2xl">エラーです</div>
        </div>{" "}
      </>
    );
  if (isLoading) {
    return (
      <>
        <LoadingUI />
      </>
    );
  }
  const onShareAsX = async () => {
    data!.map(async (text) => {
      await axios.post("/api/post", {
        content: text,
      });
    });
  };
  return (
    <>
      <div className="m-8 flex items-center justify-center flex-col">
        <h1 className="text-3xl font-bold">黒歴史を振り返る</h1>
        <div className="p-4 max-w-2xl mx-auto">
          <h1 className="text-xl font-bold text-center">あなたの黒歴史は？</h1>
          {data!.length > 0 ? (
            <ul className="list-disc list-outside bg-white p-4 rounded-md">
              {data!.map((text, index) => (
                <li key={index} className="text-gray-800 mb-2 break-words ">
                  {text}
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-center">
              <p className="text-xl text-blue-700 mt-3">
                あなたはまともな人間です
              </p>
              <img
                src="/img/decent-person.jpg"
                alt="まともな人間"
                className="mt-4 mx-auto"
              />
            </div>
          )}
        </div>
        <div className="items-center justify-center flex flex-col">
          <button className="mt-7 px-9 py-3 w-48 bg-black text-white rounded-full shadow-md hover:bg-red-600">
            リンクを共有する
          </button>
          <button
            className="mt-8 px-9 py-3 w-48 bg-black text-white rounded-full shadow-md hover:bg-red-600"
            onClick={onShareAsX}
          >
            Xに投稿する
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
