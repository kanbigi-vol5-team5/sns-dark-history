import Link from "next/link";

export const metadata = {
  title: "SNS | result",
};

export default function Page() {
  return (
    <>
      <div className="h-screen flex items-center justify-center flex-col">
        <div className="items-center justify-center flex flex-col">
          <video width="250" height="250" loop autoPlay muted>
            <source src="/img/result.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="items-center justify-center flex flex-col">
          <button className="mt-12 px-9 py-3 w-48 bg-black text-white rounded-full shadow-md hover:bg-red-600">
            黒歴史を振り返る
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
