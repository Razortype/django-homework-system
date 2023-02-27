function codeWrapper(element) {
    var parent = element.parentNode;
    var wrapper = document.createElement("div")
    wrapper.className = "code-block";

    parent.replaceChild(wrapper, element);
    wrapper.appendChild(element);

}

function replaceCodeBlocks() {
    var codeBlocks = document.getElementsByTagName("code");
    if (codeBlocks.length > 0) {
        for (let i = 0; i < codeBlocks.length; i++) {
            codeWrapper(codeBlocks[i])
        }
    }
}

replaceCodeBlocks();