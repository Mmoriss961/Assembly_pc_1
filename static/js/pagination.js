function  ajaxPagination(){
    $('#pag_1 a.page-link').each((index,el) => {
        $(el).click((e) => {
            e.preventDefault()
            let page_url = $(el).attr('href')

            let
                $pagination = $('#pagination')
                $pagination_centred = $('#pag_1')

            $.ajax({
                url:page_url,
                type: 'GET',
                success: (data) => {
                    $pagination.empty()
                    $pagination.append( $(data).find('#pagination').html() )
                    $pagination_centred.empty()
                    $pagination_centred.append( $(data).find('#pag_1').html() )
                }
            })
        })
    })
}
$(document).ready(function (){
    ajaxPagination()})
$(document).ajaxStop(function (){
    ajaxPagination()})