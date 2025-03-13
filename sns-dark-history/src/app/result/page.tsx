import Link from "next/link";

export const metadata = {
  title: "SNS | result",
};

export default function Page() {
  return (
    <>
      <h1>page</h1>
      <p>
        <Link href="/">トップへ</Link>
      </p>
    </>
  );
}
