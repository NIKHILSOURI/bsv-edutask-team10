import React, { useState } from 'react'
import Converter from './../Util/Converter'

function TaskCreator(props) {
    const [title, setTitle] = useState("")
    const [url, setUrl] = useState("")

    const submitNewTask = (event) => {
        event.preventDefault();

        const data = new URLSearchParams();
        data.append('title', title);
        data.append('description', '');
        data.append('userid', props.userid);
        data.append('url', url);
        data.append('todos', ['Watch video']);

        console.log(props.userid);

        fetch('http://localhost:5000/tasks/create', {
            method: 'post',
            body: data
        }).then(res => res.json())
            .then(tasklist => {
                let convertedTasks = [];
                for (const task of tasklist) {
                    convertedTasks.push(Converter.convertTask(task));
                }
                props.setTasks(convertedTasks);
            })
            .catch(function (error) {
                console.error(error)
            });

        setTitle("");
        setUrl("");
    }

    return (
        <form className="submit-form" onSubmit={submitNewTask}>
            <div className='inputwrapper'>
                <label>Title</label>
                <input type='text' id='title' name='title' onChange={event => setTitle(event.target.value)}></input>
            </div>
            <div className='inputwrapper'>
                <label>YouTube URL</label>
                <input type='text' id='url' name='url' onChange={event => setUrl(event.target.value)}></input>
            </div>

            <input type="submit" value="Create new Task" disabled={title.length === 0}></input>
        </form>
    )
}

export default TaskCreator