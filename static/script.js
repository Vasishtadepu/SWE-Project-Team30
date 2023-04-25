function increase_text(){
    const mom = document.getElementById('student_details')
    //before creating a new field first we need to decide on the name of
    //the input element we are going to create.
    last_child = mom.lastElementChild
    if (last_child!=null)
    {
        const name_last = last_child.getAttribute("name")
        let num = Number(name_last.slice(7))
        num++
        console.log(num)
        name_current = "Student" + num.toString()
    }
    else if (last_child==null)
    {
        name_current = "Student1"
    }
    const field = document.createElement("input")
    field.setAttribute("type","text")
    field.setAttribute("name",name_current)
    console.log(name_current)
    mom.appendChild(field)
}

function remove_text(){
    const mom = document.getElementById('student_details')
    last_child = mom.lastElementChild
    mom.removeChild(last_child)
}

function increase_approver(){
    const mom = document.getElementById('approver_details')
    //before creating a new field first we need to decide on the name of
    //the input element we are going to create.
    last_child = mom.lastElementChild
    if (last_child!=null)
    {
        const name_last = last_child.getAttribute("name")
        let num = Number(name_last.slice(7))
        num++
        console.log(num)
        name_current = "Student" + num.toString()
    }
    else if (last_child==null)
    {
        name_current = "Student1"
    }
    const field = document.createElement("input")
    field.setAttribute("type","text")
    field.setAttribute("name",name_current)
    console.log(name_current)
    mom.appendChild(field)
}

function decrease_approver(){
    const mom = document.getElementById('approver_details')
    last_child = mom.lastElementChild
    mom.removeChild(last_child)
}