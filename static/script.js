window.addEventListener("DOMContentLoaded", function () {
    window.addEventListener("load", function () {
        document.body.classList.remove("preload")
    })



    let theme = localStorage.getItem('theme') 

    if (theme == null || theme != 'dark') {
        localStorage.setItem('theme', 'light')
    } else {
        document.body.classList.add("dark-theme")
    }
 




    if (document.getElementById("editor-body") !== null) {
        // tagarea input
        const contentSection = document.querySelector("#editor-input-content")
        const tagArea = document.querySelector("#editor-tagarea")

        // navbar btns
        const para_new_btn = document.querySelector("#para_btn")
        const code_new_btn = document.querySelector("#code_btn")
        const img_new_btn = document.querySelector("#img_btn")
        const vid_new_btn = document.querySelector("#vid_btn")

        // hamburger and nav bar
        const sliderBurger = document.querySelector("#editor-hamburger")
        const sliderNav = document.querySelector("#editor-slider-nav")
        const fixedBtn = document.querySelector('.fixed-btns')

        // tagarea children
        const tagUl = tagArea.children[0]
        const tagText = tagArea.children[1]

        let itemHeight = 40
        let divHeight = 40


        // listener - btns
        para_new_btn.onclick = function () {
            newEditorPara()
        }
        code_new_btn.onclick = function () {
            newEditorCode()
        }
        img_new_btn.onclick = function () {
            newEditorImg()
        }
        vid_new_btn.onclick = function () {
            newEditorVid()
        }

        // listener - burger click
        sliderBurger.addEventListener("click", function () {
            burgerMove()
        })

        // listener - tag space
        tagArea.addEventListener("keydown", function (e) {
            if (e.code == "Space") {
                e.preventDefault()
                newEditorTag()
            }
        })

        // listener - input
        contentSection.addEventListener("input", function (e) {
            // textarea
            if (e.target.parentElement.classList.contains("editor-textarea")) {
                e.target.nextElementSibling.innerHTML = e.target.value + "\r\n"
            }

            // codearea
            if (e.target.parentElement.classList.contains("editor-codearea")) {
                e.target.nextElementSibling.innerHTML = e.target.value
            }

            // imgarea
            if (
                e.target.parentElement.parentElement.classList.contains(
                    "editor-imgarea"
                )
            ) {
                if (e.target.files && e.target.files[0]) {
                    const reader = new FileReader()

                    reader.onload = function (e2) {
                        imgTag =
                            e.target.parentElement.parentElement.children[2]
                        imgTag.setAttribute("src", e2.target.result)
                    }
                    reader.readAsDataURL(e.target.files[0])
                }
            }

            // vidarea
            if (
                e.target.parentElement.parentElement.classList.contains(
                    "editor-vidarea"
                )
            ) {
                if (e.target.files && e.target.files[0]) {
                    vidNameTag =
                        e.target.parentElement.parentElement.children[2]
                    vidNameTag.textContent = e.target.files[0].name
                }
            }
        })

        // listener - keyup
        contentSection.addEventListener("keyup", function (e) {
            // textarea
            if (e.target.parentElement.classList.contains("editor-textarea")) {
                if (e.code == "Backspace" && e.target.value == "") {
                    e.preventDefault()
                    if (!!e.target.parentElement.previousElementSibling) {
                        e.target.parentElement.previousElementSibling.children[0].focus()
                        e.target.parentElement.remove()
                    } else {
                        e.target.parentElement.remove()
                    }
                }
            }

            // codearea
            if (e.target.parentElement.classList.contains("editor-codearea")) {
                if (e.code == "Backspace" && e.target.value == "") {
                    e.preventDefault()
                    if (!!e.target.parentElement.previousElementSibling) {
                        e.target.parentElement.previousElementSibling.children[0].focus()
                        e.target.parentElement.remove()
                    } else {
                        e.target.parentElement.remove()
                    }
                }
            }
        })

        // listener - keydown
        contentSection.addEventListener("keydown", function (e) {
            // textarea
            if (e.target.parentElement.classList.contains("editor-textarea")) {
                if (e.code == "Enter") {
                    e.preventDefault()
                    newEditorPara()
                }
            }

            // codearea
            if (e.target.parentElement.classList.contains("editor-codearea")) {
                if (e.code == "Enter") {
                    e.preventDefault()
                    e.target.value += "\r\n"
                    itemHeight = itemHeight + 21
                    divHeight = divHeight + 21
                    e.target.style.height = itemHeight + "px"
                    e.target.nextElementSibling.style.height = divHeight + "px"
                }

                if (e.code == "Backspace") {
                    if (
                        e.target.nextElementSibling.textContent.endsWith("\n")
                    ) {
                        itemHeight = itemHeight - 21
                        divHeight = divHeight - 21
                        e.target.style.height = itemHeight + "px"
                        e.target.nextElementSibling.style.height =
                            divHeight + "px"
                    }
                }
            }

            // tagarea
            if (e.target.parentElement.classList.contains("editor-tagarea")) {
                if (e.code == "Space") {
                    e.preventDefault()
                    newEditorTag()
                }
            }
        })

        // function - new paragraph
        function newEditorPara() {
            let para_html = document.createElement("div")
            para_html.className = "editor-textarea"

            para_html.appendChild(document.createElement("textarea"))
            para_html.appendChild(document.createElement("div"))
            para_html.children[0].setAttribute("placeholder", "Enter text here")

            let editor_para_html = contentSection.appendChild(para_html)
            editor_para_html.children[0].focus()
        }

        // function - new codebox
        function newEditorCode() {
            let codebox_html = document.createElement("div")
            codebox_html.className = "editor-codearea"
            codebox_html.appendChild(document.createElement("textarea"))
            codebox_html.appendChild(document.createElement("div"))
            codebox_html.children[0].setAttribute(
                "placeholder",
                "Enter code here"
            )

            let editor_codebox_html = contentSection.appendChild(codebox_html)
            editor_codebox_html.children[0].focus()
        }

        // function - new image
        function newEditorImg() {
            let img_html = document.createElement("div")
            img_html.className = "editor-imgarea"

            img_html.appendChild(document.createElement("label"))
            img_html.appendChild(document.createElement("div"))
            img_html.appendChild(document.createElement("img"))

            img_html.children[0].setAttribute("for", `img-input`)
            img_html.children[0].innerHTML = "Upload Image"
            img_html.children[0].appendChild(document.createElement("input"))
            img_html.children[0].children[0].setAttribute("type", "file")
            img_html.children[0].children[0].id = `img-input`
            img_html.children[1].className = "close icon"

            let editor_img_html = contentSection.appendChild(img_html)
            editor_img_html.children[1].onclick = function () {
                editor_img_html.remove()
            }
        }

        // function - new video
        function newEditorVid() {
            let vid_html = document.createElement("div")
            vid_html.className = "editor-vidarea"

            vid_html.appendChild(document.createElement("label"))
            vid_html.appendChild(document.createElement("div"))
            vid_html.appendChild(document.createElement("p"))

            vid_html.children[0].setAttribute("for", `vid-input`)
            vid_html.children[0].textContent = "Upload Video"
            vid_html.children[0].appendChild(document.createElement("input"))
            vid_html.children[0].children[0].setAttribute("type", "file")
            vid_html.children[0].children[0].id = `vid-input`
            vid_html.children[1].className = "close icon"

            let editor_vid_html = contentSection.appendChild(vid_html)
            editor_vid_html.children[1].onclick = function () {
                editor_vid_html.remove()
            }
        } 

        // function - burger nav movement
        function burgerMove() {
            if (sliderNav.classList.contains("active")) {
                fixedBtn.classList.add('active')
                sliderNav.classList.remove("active")
                sliderBurger.classList.remove("active")
            } else {
                fixedBtn.classList.remove('active')
                sliderNav.classList.add("active")
                sliderBurger.classList.add("active")
            }
        }

        // function - add and remove tags
        function newEditorTag() {
            text = tagText.value
            tagText.value = ""

            let newTag = document.createElement("li")
            let link = document.createElement("a")
            let span = document.createElement("span")

            span.innerHTML = "#"
            link.innerHTML = link.innerHTML + text

            newTag.appendChild(span)
            newTag.appendChild(link)
            let new_tag_html = tagUl.appendChild(newTag)

            new_tag_html.addEventListener("click", function () {
                new_tag_html.remove()
            })
        }
    }

    if (document.getElementById("tag-body") !== null) {
        const btnContainer = document.querySelector("#tag-body-header-nav")
        const tagContent = document.querySelector("#tag-content")

        // Tag sticky navigation on mobile
        const tagNavbar = document.querySelector("#tag-body-header-nav")
        const tagHeader = document.querySelector("#tag-body-header-h1")
        const sticky = tagNavbar.offsetTop

        // listen - tag btn click
        btnContainer.addEventListener("click", function (e) {
            tagNavMove(e)
        })

        // listen - mobile scroll
        document.addEventListener("scroll", function () {
            tagNavSticky()
        })

        // function - tag nav movement
        function tagNavMove(e) {
            if (e.target.parentElement.classList.contains("btn")) {
                for (let btn of btnContainer.children) {
                    if (btn == e.target.parentElement) {
                        if (!btn.classList.contains("active")) {
                            btn.classList.add("active")
                            let currentTag = btn.classList[0]

                            for (let ul of tagContent.children) {
                                if (
                                    ul.classList.contains(
                                        currentTag + "-content"
                                    )
                                ) {
                                    if (!ul.classList.contains("active")) {
                                        ul.classList.add("active")
                                    }
                                } else if (ul.classList.contains("active")) {
                                    ul.classList.remove("active")
                                }
                            }
                        }
                    } else if (btn.classList.contains("active")) {
                        btn.classList.remove("active")
                    }
                }
            }
        }

        // function - tag nav mobile ui
        function tagNavSticky() {
            if (window.pageYOffset >= sticky) {
                tagHeader.classList.add("sticky-head")
                tagNavbar.classList.add("sticky")
            } else {
                tagHeader.classList.remove("sticky-head")
                tagNavbar.classList.remove("sticky")
            }
        }
    }

    if (document.getElementById("index-body") !== null) {
        let switcher = document.querySelector('#theme-switch')
        let indexNav = document.getElementById("index-body-header-nav")

        const pagination_area = document.querySelector('.pagination')
        const pagination_page = Number(pagination_area.querySelector('.num').textContent)
        const pagination_last = Number(pagination_area.id)
        paginator()




        // listener - theme switcher
        switcher.addEventListener('click', function () {
            if (localStorage.theme == 'dark') {
                localStorage.theme = 'light'
                document.body.classList.remove("dark-theme")
            } else {
                localStorage.theme = 'dark'
                document.body.classList.add("dark-theme")
            }
        })

        // listener - mobile nav animation
        window.addEventListener("scroll", function () {
            if (
                document.body.scrollTop > 150 ||
                document.documentElement.scrollTop > 150
            ) {
                indexNav.style.top = "0"
            } else {
                indexNav.style.top =
                    "-100px"
            }
        })

        // function - pagination deactivate and links
        function paginator() {
            if (pagination_page == 1) {
                pagination_area.children[0].classList.add('deactivate')
                pagination_area.children[0].children[0].removeAttribute('href')
            } else {
                pagination_area.children[0].children[0].setAttribute('href', `/page?n=${pagination_page - 1}`)
            }

            if (pagination_page == pagination_last + 1) {
                pagination_area.children[2].classList.add('deactivate')
                pagination_area.children[2].children[0].removeAttribute('href')
            } else {
                pagination_area.children[2].children[0].setAttribute('href', `/page?n=${pagination_page + 1}`)
                console.log(pagination_area.children[2].children[0])
            }
        }
    }

    if (document.getElementById("archive-body") !== null) {
        // function loadDoc() {
        //     const xhr = new XMLHttpRequest()
        //     xhr.open('GET', '/archive-2', true)

        //     xhr.onload = function() {
        //         if (this.status === 200) {
        //             console.log(this.responseText)
        //         }
        //     }
        //     xhr.send()
        // }

        // let thing = document.querySelector('#somethingbig')
        // thing.addEventListener('click', function() {
        //     loadDoc()
        //   })
    }

    if (document.getElementById("login-body") !== null) {
        const error_alerts = document.querySelector('.errors')

        if (error_alerts.children[0]) {
            error_alerts.style.opacity = 1
            setTimeout(opac, 4000)
            function opac() {
                error_alerts.style.opacity = 0
            }
        }
    }

})