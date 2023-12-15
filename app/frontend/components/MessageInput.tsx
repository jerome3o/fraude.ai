import '../app/globals.css'

import { useState } from 'react'

const MessageInput = (
    { sendMessage }: { sendMessage: (message: string) => void }
) => {
    const [message, setMessage] = useState('')

    const handleSend = () => {
        sendMessage(message)
        console.log(message)
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
