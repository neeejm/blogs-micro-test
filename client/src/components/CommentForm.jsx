import axios from "axios"
import { useState } from "react"
import { BASE_URL } from "../constants"

const CommentForm = ({ postId }) => {
    const [comment, setComment] = useState("")

    const doComment = (event) => {
        event.preventDefault()

        axios.post(`${BASE_URL}/posts/${postId}/comments`, {
            "content": comment
        })
            .then(setComment(""))
            .catch(error => console.error(error))
    }

    return (
        <form onSubmit={doComment}>
            <input type="text" className="input" value={comment} onChange={event => setComment(event.target.value)} />
            <button className="button is-small is-capitalized is-primary is-light">comment</button>
        </form>
    )
}

export default CommentForm