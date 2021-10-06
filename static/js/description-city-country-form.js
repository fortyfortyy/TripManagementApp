        let descriptionForm = document.querySelectorAll(".js-description-form")
        let descriptionContainer = document.querySelector("#form-container")
        let descriptionAddButton = document.querySelector("#add-description-form")
        let descriptionTotalForms = document.querySelector("#id_descriptions-TOTAL_FORMS")

        let descriptionFormNum = descriptionForm.length-1
        descriptionAddButton.addEventListener('click', descriptionAddForm)

        function descriptionAddForm(e){
            e.preventDefault()

            let newForm = descriptionForm[0].cloneNode(true)
            let formRegex = RegExp(`descriptions-(\\d){1}-`,'g')

            descriptionFormNum++

            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `descriptions-${descriptionFormNum}-`)
            newForm.querySelectorAll('label')[0].innerHTML = ""
            newForm.querySelector(`#id_descriptions-${descriptionFormNum}-content`).value = ""

            descriptionContainer.insertBefore(newForm, descriptionAddButton)

            descriptionTotalForms.setAttribute('value', `${descriptionFormNum+1}`)
        }

        let cityForm = document.querySelectorAll(".js-city-form")
        let cityContainer = document.querySelector("#city-container")
        let cityAddButton = document.querySelector("#add-city-form")
        let cityTotalForms = document.querySelector("#id_cities-TOTAL_FORMS")

        let cityFormNum = cityForm.length-1
        cityAddButton.addEventListener('click', cityAddForm)

        function cityAddForm(e){
            e.preventDefault()

            let newForm = cityForm[0].cloneNode(true)
            let formRegex = RegExp(`cities-(\\d){1}-`,'g')

            cityFormNum++
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `cities-${cityFormNum}-`)
            newForm.querySelector(`#id_cities-${cityFormNum}-city`).value = ""

            cityContainer.insertBefore(newForm, cityAddButton)

            cityTotalForms.setAttribute('value', `${cityFormNum+1}`)
        }

        let countryForm = document.querySelectorAll(".js-country-form")
        let countryContainer = document.querySelector("#country-container")
        let countryAddButton = document.querySelector("#add-country-form")
        let countryTotalForms = document.querySelector("#id_countries-TOTAL_FORMS")

        let countryFormNum = countryForm.length-1
        countryAddButton.addEventListener('click', countryAddForm)

        function countryAddForm(e){
            e.preventDefault()

            let newForm = countryForm[0].cloneNode(true)
            let formRegex = RegExp(`countries-(\\d){1}-`,'g')

            countryFormNum++
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `countries-${countryFormNum}-`)
            newForm.querySelector(`#id_countries-${countryFormNum}-country`).value = ""

            countryContainer.insertBefore(newForm, countryAddButton)

            countryTotalForms.setAttribute('value', `${countryFormNum+1}`)
        }
