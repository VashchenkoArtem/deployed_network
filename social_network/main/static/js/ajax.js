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

    $.ajax({
        url: `/get_info/`,
        type: "get",
        success: function(response){
            $(".posts-count").text(response.all_posts_count);
            $(".readers").text(response.all_views);
            $(".friends-count").text(response.my_friends);
        }
    });
    let page = 1;
    let isLoading = false;

    function loadMorePosts() {
        if (isLoading) return;
        isLoading = true;
        page += 1;

        $.ajax({
            url: `/load_posts/?page=${page}`,
            type: "GET",
            success: function(data) {
                if (data.trim().length > 0) {
                    $(".posts").append(data);
                    isLoading = false;
                }
            }
        });
    }

    let observer = new IntersectionObserver(function(entries) {
        if (entries[0].isIntersecting) {
            loadMorePosts();
        }
    }, {
        rootMargin: '100px'
    });

    observer.observe(document.querySelector("#load-more-trigger"));
});