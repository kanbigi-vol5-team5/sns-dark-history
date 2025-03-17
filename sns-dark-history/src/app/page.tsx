export default function Page() {
  return (
    <>
      <div className="h-screen bg-cover bg-center bg-[url('/img/background2.png')]">
        <h1 className="text-4xl items-center justify-center flex pt-20 font-bold">
          SNS黒歴史クリーナー
        </h1>
        <div className="flex flex-col items-center justify-center min-h-screen">
          <input
            type="text"
            //value={username}
            //onChange={(e) => setUsername(e.target.value)}
            placeholder="ユーザーネームを入力"
            className="py-2 px-15 border rounded-xl shadow-sm text-center focus:outline-none focus:ring-2 focus:ring-red-600"
          />
          <button
            //onClick={handleClear}
            className="mt-4 px-8 py-2 bg-black text-white rounded-full shadow-md hover:bg-red-600"
          >
            消去していく
          </button>
        </div>
      </div>
    </>
  );
}
