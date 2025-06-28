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
            let requestsFrame = JSON.parse(response.all_requests);
            if (requestsFrame){
                requestsFrame.forEach(request, ()=>{
                    console.log(request.profile1.profile)
                })
            }
            // if (response.all_messages){
            //     let allMessages = JSON.parse(response.all_messages);
            //     let currentUser = $(".username-input").val()
            //     for (let count = 0; count < allMessages.length; count ++){
            //         let messageFrame = $(".message-frame");
            //         let message = allMessages[count];
            //         console.log(message.fields.profile1);
            //         console.log(message.fields.profile2);
            //         console.log(response.profile_id);
            //         if (message.fields.profile1 == response.profile_id){
            //             let messageProfile = $("<div>", {
            //                 'class': 'one-people'
            //             })
            //             let peopleInformation = $("<div>", {
            //                 'class': 'people-information'
            //             })
            //             let iconPeople = $("<div>", {
            //                 'class': 'icon-people'
            //             })
            //             let avatar = $("<img>", {
            //                 "class": "post-friend-avatar",
            //                 "src": ""
            //             })
            //             let peopleNameAndMessage = $("<a>", {
            //                 "class": "people-name-and-message",
            //                 "href": ""
            //             })
            //             let peopleNameAndTime = $("<div>", {
            //                 "class": "people-name-and-time"
            //             })
            //             let peopleName = $("<h3>", {
            //                 "class": "friend-name",
            //                 "text": message.fields
            //             })
            //             messageFrame.append(messageProfile)
            //             messageProfile.append(peopleInformation)
            //             peopleInformation.append(iconPeople)
            //             iconPeople.append(avatar)
            //             peopleInformation.append(peopleNameAndMessage)
            //             peopleNameAndMessage.append(peopleNameAndTime)
            //             peopleNameAndTime.append(peopleName)
            //         }
            //         else if (message.fields.profile2 == response.profile_id){
            //             let messageProfile = $("<div>", {
            //                 'class': 'one-people'
            //             })
            //             let peopleInformation = $("<div>", {
            //                 'class': 'people-information'
            //             })
            //             let iconPeople = $("<div>", {
            //                 'class': 'icon-people'
            //             })
            //             let avatar = $("<img>", {
            //                 "class": "post-friend-avatar",
            //                 "src": ""
            //             })
            //             let peopleNameAndMessage = $("<a>", {
            //                 "class": "people-name-and-message",
            //                 "href": ""
            //             })
            //             let peopleNameAndTime = $("<div>", {
            //                 "class": "people-name-and-time"
            //             })
            //             let peopleName = $("<h3>", {
            //                 "class": "friend-name",
            //                 "text": message.fields
            //             })
            //             messageFrame.append(messageProfile)
            //             messageProfile.append(peopleInformation)
            //             peopleInformation.append(iconPeople)
            //             iconPeople.append(avatar)
            //             peopleInformation.append(peopleNameAndMessage)
            //             peopleNameAndMessage.append(peopleNameAndTime)
            //             peopleNameAndTime.append(peopleName)
            //         }
            //     }
            // }
        }
    })

});
