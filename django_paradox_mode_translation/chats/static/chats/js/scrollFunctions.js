

function scrollToPosition(elementId, chatUrl) {
    const element = $('#' + elementId)

    const scrollTo = element.position().top + (element.parent().height / 2)
    console.log(scrollTo)
    $('#collapse-' + chatUrl).scrollTop(scrollTo)
}
