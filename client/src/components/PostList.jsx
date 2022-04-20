import CommentForm from "./CommentForm"
import { useState, useEffect } from "react";
import axios from "axios";
import CommentsList from "./CommentsList";
import { BASE_URL } from "../constants";

const PostList = () => {
    const [posts, setPosts] = useState([])

    const fetchPosts = () => {
        axios.get(BASE_URL + "/posts")
            .then((res => {
                setPosts(res.data)
            }))
            .catch(error => console.log(error))
    }

    const renderPosts = Object.values(posts).map(post => {
        return (
            <div
                className="box"
                key={post.id}>
                <h4 className="is-size-5 is-Cappitalized">{post.title}</h4>
                <p>{post.content}</p>
                <hr />
                <CommentsList comments={post.comments} />
                <hr />
                <CommentForm postId={post.id} />
            </div>
        )
    })

    useEffect(() => {
        fetchPosts()
    }, [])

    return (
        <div>
            {renderPosts}
        </div>
    )
}

export default PostList