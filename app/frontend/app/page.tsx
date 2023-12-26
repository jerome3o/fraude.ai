import ChatApp from "../components/ChatApp";
import Script from "next/script";

// TODO: need to double check how the Script should be used

export default function Home() {
  return (
    <main>
      <Script src="https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js" />
      <div id="header">
        <h1>
          <i>Fr</i>aude
        </h1>
      </div>
      <div id="main">
        <ChatApp></ChatApp>
      </div>
      <div id="footer"></div>
    </main>
  );
}
