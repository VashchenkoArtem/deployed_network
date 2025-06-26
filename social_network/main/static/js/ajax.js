$(document).ready(function(){
    $(".icon-like").each(function(element){
        $(this).on('click', function(){
            let id = this.id;
            let classObject = $(this).attr("class").split(' ')[2]
            console.log(classObject)
            $.ajax({
                url: id,
                type: "get",
                success: function(){
                    let likes = $(`#likesPost-${classObject}`);
                    console.log(likes)
                    let updatedLikes = Number(likes.text()) + 1
                    likes.text(updatedLikes)
                }
            })
        })
    });
    $(".image-confirm-tag").on("click", function(){
        let inputValue = $(".add-tag").val().split('#')[1]
        $.ajax({
            url: `/my_publications/create_tag/${inputValue}`,
            type: "get",
            success: function(){
                $(".add-tag").toggleClass("hidden");
                $(".image-confirm-tag").toggleClass("hidden");
                let newElement = $('<label type = "button" class="tag-object"></label>');
                newElement.text(`#${inputValue}`);
                let div = $(".tag-container");
                let elementInDiv = div.children();
                elementInDiv.eq(-3).before(newElement)
            }
        })
    })
});
