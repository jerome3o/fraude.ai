import ChatApp from '../components/ChatApp'

export default function Home() {
  return (
    <main>
      <div id='header'>
        <h1><i>Fr</i>aude</h1>
      </div>
      <div id='main'><ChatApp></ChatApp></div>
      <div id='footer'></div>
    </main>
  )
}
