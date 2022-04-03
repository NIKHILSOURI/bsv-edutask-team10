module.exports = {
    convertTask: function (taskobj) {
        let todolist = []
        for (const todo of taskobj.todos) {
            todolist.push({
                _id: todo['_id']['$oid'],
                description: todo.description,
                done: todo.done
            })
        }

        let task = {
            _id: taskobj['_id']['$oid'],
            title: taskobj.title,
            description: taskobj.description,
            url: taskobj.video.url,
            todos: todolist
        }

        return task;
    }
}