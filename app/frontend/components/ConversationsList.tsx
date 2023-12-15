import '../app/globals.css'


import { ConversationHeaders } from '../fraude/apiService'

const ConversationList = (
    { conversations }: { conversations: ConversationHeaders }
) => {
    return (
        <div className='conversations-list debug'>
            <h3>Conversations</h3>
            <div className='conversations-list-inner'>
                {conversations.map((info) => { return <button key={info.id}>{info.title}</button> })}
            </div>
        </div>
    )
}

export default ConversationList
