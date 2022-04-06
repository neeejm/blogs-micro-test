import { useState } from "react"
import axios from "axios"

const PostForm = () => {
    const [title, setTitle] = useState("")
    const [content, setContent] = useState("")

    const doPost = (event) => {
        event.preventDefault()

        axios.post("http://localhost:8000/posts", {
            title,
            content
        }).then()

        setTitle("")
        setContent("")
    }

    return (
        <div className="container" onSubmit={doPost}>
            <form>
                <div className="field">
                    <label className="is-size-4 is-capitalized">title: </label>
                    <input
                        className="input"
                        type="text"
                        placeholder="post title"
                        value={title}
                        onChange={event => {
                            setTitle(event.target.value)
                        }} />
                </div>

                <div className="field">
                    <label className="is-size-4 is-capitalized">content: </label>
                    <textarea
                        className="textarea"
                        placeholder="e.g Hello World"
                        value={content}
                        onChange={event => {
                            setContent(event.target.value)
                        }} />
                </div>

                <button className="button is-medium is-primary is-light">Post</button>
            </form>
        </div>
    )
}

export default PostForm