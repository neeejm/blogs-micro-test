import PostForm from "./components/PostForm"
import PostList from "./components/PostList"

const App = () => {
    return (
        <div className="container">
            <h1 className="is-size-2 m-5">Welcome to Blogs</h1>

            <div className="container box">
                <h3 className="is-size-4">Posting</h3>
                <hr />
                <PostForm />
            </div>

            <div className="container mt-4">
                <h3 className="is-size-4">Posts</h3>
                <hr />
                <PostList />
            </div>
        </div>
    )
}

export default App