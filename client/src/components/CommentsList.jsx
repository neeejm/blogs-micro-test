import axios from "axios"
// import { useEffect, useState } from "react"

const CommentsList = ({ comments }) => {
    // const [comments, setComments] = useState([])

    // const fetchComments = () => {
    //     axios.get(`http://localhost:8001/posts/${postId}/comments`)
    //         .then(response => {
    //             setComments(response.data)
    //         })
    //         .catch(error => console.error(error))
    // }

    // useEffect(() => {
    //     fetchComments()
    // }, [])

    const renderComments = Object.values(comments).map(comment => {
        switch (comment.status) {
            case "pending":
                comment.content = "waiting moderation!"
                break;
            case "reject":
                comment.content = "comment rejected!"
                break;
            default:
        }
        return (
            <li key={comment.id}>{comment.content}</li>
        )
    })


    return (
        <div className="content">
            <ul className="">
                {renderComments}
            </ul>
        </div>
    )
}

export default CommentsList