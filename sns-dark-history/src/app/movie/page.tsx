import Link from "next/link";

export const metadata = {
  title: "SNS | movie",
};
const texts = [];

export default function Page() {
  return (
    <>
      <div className="m-8 flex items-center justify-center flex-col">
        <h1 className="text-3xl font-bold">黒歴史を振り返る</h1>
        <div className="p-4 max-w-2xl mx-auto">
          <h1 className="text-xl font-bold text-center">あなたの黒歴史は？</h1>
          {texts.length > 0 ? (
            <ul className="list-disc list-inside bg-white p-4 rounded-md">
              {texts.map((text, index) => (
                <li key={index} className="text-gray-800 mb-2">
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
          <button className="mt-8 px-9 py-3 w-48 bg-black text-white rounded-full shadow-md hover:bg-red-600">
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
