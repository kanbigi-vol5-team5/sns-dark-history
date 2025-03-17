//import Link from "next/link";

export const metadata = {
  title: "SNS | loading",
};

export default function Page() {
  return (
    <>
      <div className="items-center justify-center flex flex-col min-h-screen">
        <video width="300" height="300" loop autoPlay muted>
          <source src="/img/loading.mp4" type="video/mp4" />
          動画が表示されていません
        </video>
      </div>
    </>
  );
}
