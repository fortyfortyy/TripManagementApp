    let tagForm = document.querySelectorAll(".js-tags-form")
    let tagContainer = document.querySelector("#tag-container")
    let tagAddButton = document.querySelector("#add-tags-form")
    let tagTotalForms = document.querySelector("#id_tags-TOTAL_FORMS")

    let tagFormNum = tagForm.length-1
    tagAddButton.addEventListener('click', tagAddForm)

    function tagAddForm(e){
        e.preventDefault()

        let newForm = tagForm[0].cloneNode(true)
        let formRegex = RegExp(`tags-(\\d){1}-`,'g')

        tagFormNum++
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `tags-${tagFormNum}-`)
        newForm.querySelector(`#id_tags-${tagFormNum}-tag`).value = "#"
        tagContainer.insertBefore(newForm, tagAddButton)

        tagTotalForms.setAttribute('value', `${tagFormNum+1}`)
    }