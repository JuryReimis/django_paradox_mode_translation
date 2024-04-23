

function scrollToPosition(elementId, chatUrl) {
    const element = $('#' + chatUrl + '-' + elementId)
    if (element.length) {
        const scrollTo = element.position().top - (element.parent().height() / 2)
        console.log('element at', element.position().top)
        console.log('scroll to', scrollTo)
        $('#collapse-' + chatUrl).scrollTop(scrollTo)
    }
}
