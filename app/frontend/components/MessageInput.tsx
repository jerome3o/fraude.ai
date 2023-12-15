import '../app/globals.css'

import { useState } from 'react'

const MessageInput = (
    { sendMessage }: { sendMessage: (message: string) => Promise<void> }
) => {
    const [message, setMessage] = useState('')

    async function handleSend() {
        await sendMessage(message)
        setMessage('')
    }

    return (
        <div className='message-input debug' >
            <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} />
            <button onClick={handleSend}>Send</button>
        </div >
    )
}

export default MessageInput
