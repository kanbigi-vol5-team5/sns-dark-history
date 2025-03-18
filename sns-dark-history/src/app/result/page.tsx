import Link from "next/link";

export const metadata = {
  title: "SNS | result",
};

export default function Page() {
  return (
    <>
      <div className="h-screen flex items-center justify-center flex-col">
        <div className="items-center justify-center flex flex-col">
          <img src="/img/image_fx_.jpg"></img>
        </div>
        <h1 className="text-2xl font-bold">黒歴史の判定が終わりました</h1>
        <div className="items-center justify-center flex flex-col">
          <Link href="/movie">
            <button className="mt-12 px-9 py-3 w-48 bg-black text-white rounded-full shadow-md hover:bg-red-600">
              黒歴史を振り返る
            </button>
          </Link>
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
