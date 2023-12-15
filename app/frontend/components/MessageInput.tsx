import '../app/globals.css'

import { useState } from 'react'

const MessageInput = (
    { sendMessage }: { sendMessage: (message: string) => Promise<void> }
) => {
    const [message, setMessage] = useState('')

    async function handleSend(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        setMessage('')
        await sendMessage(message)
    }

    return (
        <form onSubmit={handleSend} className='message-input'>
            <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} />
            <button type="submit">Send</button>
        </form>
    )
}

export default MessageInput
