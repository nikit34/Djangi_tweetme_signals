import React, {useEffect, useState} from 'react'


function loadTweets(callback) {
    const xhr = new XMLHttpRequest()
    const method = 'GET'
    const url = 'http://localhost:8000/api/tweets/'
    xhr.responseType = 'json'
    xhr.open(method, url)
    xhr.onload = function () {
        callback(xhr.response, xhr.status)
    }
    xhr.onerror = function (e) {
        console.log(e)
        callback({'message': 'The request was an error'}, 400)
    }
    xhr.send()
}

export function TweetsList(props) {
    const [tweets, setTweets] = useState([])

    useEffect(() => {
        const myCallback = (response, status) => {
            if(status === 200){
                setTweets(response)
            } else {
                alert('Set Tweets has not been')
            }
        }
        loadTweets(myCallback)
    }, [])
    return tweets.map((item, index)=>{
        return <Tweet tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`} />
    })
}

export function ActionBtn(props) {
    const {tweet, action} = props
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    return action.type === 'like' ? <button className={className}>{tweet.likes} Like</button> : null
}

export function Tweet(props) {
    const {tweet} = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className={className}>
        <p>{tweet.id} - {tweet.content}</p>
        <div className='btn btn-group'>
            <ActionBtn tweet={tweet} action={{type: "like"}}/>
            <ActionBtn tweet={tweet} action={{type: "unlike"}}/>
        </div>
    </div>
}
