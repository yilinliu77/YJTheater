var total_vote = 0;
//var vote_1 = 0;
//var vote_2 = 0;
//var vote_3 = 0;
//var vote_4 = 0;
//var vote_5 = 0;
//var vote_6 = 0;

var voteCount = 0;

function vote() {
    var selectItem = 0;
    var items = document.getElementsByName("item");

    for(i=0; i<items.length; i++){
        if(items[i].checked){
            selectItem++;
            total_vote++;
//            switch(parseInt(items[i].value)){
//                case 1: vote_1++;break;
//                case 2: vote_2++;break;
//                case 3: vote_3++;break;
//                case 4: vote_4++;break;
//                case 5: vote_5++;break;
//                case 6: vote_6++;break;
//
            voteCount = parseInt(items[i].value);
        }
    }

    if(selectItem<=0){
        alert("请先选择你想看的电影111");
        return;
    }

    //和服务器建立连接
    mySocket = io.connect();
    mySocket.emit('vote', voteCount);

    alert("投票成功！");

    //计算票数占比
    // var vote1_num = new Number(vote_1/total_vote);
    // var vote2_num = new Number(vote_2/total_vote);
    // var vote3_num = new Number(vote_3/total_vote);
    // var vote4_num = new Number(vote_4/total_vote);
    // var vote5_num = new Number(vote_5/total_vote);
    // var vote6_num = new Number(vote_6/total_vote);

    // setVoteResult(vote_1, vote1_num, total_vote, 1);
    // setVoteResult(vote_2, vote2_num, total_vote, 2);
    // setVoteResult(vote_3, vote3_num, total_vote, 3);
    // setVoteResult(vote_4, vote4_num, total_vote, 4);
    // setVoteResult(vote_5, vote5_num, total_vote, 5);
    // setVoteResult(vote_6, vote6_num, total_vote, 6);

    // for(i=0; i<items.length; i++){
    //     items[i].checked = false;
    // }

    // //显示投票结果及百分比
    // function setVoteResult(vote, vote_num, total_num, type) {
    //     var _span = document.getElementById("span" + type);
    //     _span.innerHTML = vote;

    //     var total = document.getElementById("span1" + type);
    //     total.innerHTML = total_num;

    //     var _span1 = document.getElementById("span11" + type);
    //     var _percent = new Number(100*vote_num)
    //     _span1.innerHTML = _percent.toFixed(1) + "%";
    // }

}


