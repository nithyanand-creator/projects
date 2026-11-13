const result = document.getElementById("result");
const result2 =document.getElementById("result2");
const button = document.getElementById("change");
const answer = document.getElementsByName("answer");
const correctanswer = "a";
const score = document.getElementById("score");
const answer2 = document.getElementsByName("answer2");
const correctanswer2 = "JavaScript";
button.addEventListener("click", function()
{
    let selectedanswer = "";
    let selectedanswer2 = "";
    let count = 0;
    let count2 = 0;
    let total = 0;
    for(let i=0; i<answer.length; i++)
    {
        if(answer[i].checked)
        {
            selectedanswer = answer[i].value;
            break;
        }
        else count++;
    }
    for(let j=0; j<answer2.length; j++)
    {
        if(answer2[j].checked)
        {
            selectedanswer2 = answer2[j].value;
            break;
        }
        else count2++;
    }
    if(selectedanswer === correctanswer)
    {
        result.textContent = "Correct!";
        total++;
    }
    else if(count === 4) result.textContent = "Please select an answer!";
    else result.textContent = "Wrong!";

    if(selectedanswer2 === correctanswer2)
    {
        result2.textContent = "Correct!";
        total++;
    }
    else if(count2 === 4) result2.textContent = "Please select an answer!";
    else result2.textContent = "Wrong!";

    if(total === 2)
    {
        score.textContent = "Score: 2 / 2";
    }
    else if(total === 1) score.textContent = "Score: 1 / 2";

    else if(total === 0) score.textContent = "Score: 0 / 2";

});