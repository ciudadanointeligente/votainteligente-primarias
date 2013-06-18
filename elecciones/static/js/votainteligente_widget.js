var static_url = 'http://votainteligente-primarias2.s3-website-us-east-1.amazonaws.com';
var pintaElRanking = function(){
	$('head').append('<link href="'+static_url+'/ranking_widget.css" rel="stylesheet">');
        var url = 'http://www.votainteligente.cl/ranking.json?callback=readData';
	$('head').append('<script src="'+url+'"></script>');
}
var readData = function(data){
                $('.votainteligente').append("<div class=\"thumbnail tituloRanking\" ><img src=\""+static_url+"/images/angel.png\" alt=\"\" /><br />Estos son los candidatos que <strong>MÁS</strong> responden a los ciudadanos<div class='buenos'><ul></ul></div></div>");
                $('.votainteligente').append("<div class=\"thumbnail tituloRanking\" ><img src=\""+static_url+"/images/diablo.png\" alt=\"\" /><br />Estos son los candidatos que <strong>MENOS</strong> responden a los ciudadanos<div class='malos'><ul></ul></div></div>");

                
                for(var i=0;i<data.malos.length;i++){
                        $(".votainteligente .malos ul").append("<li class=\"itemListadoCandidatos\">"+data.malos[i].candidato+" no ha respondido "+data.malos[i].preguntas_no_respondidas+" de "+data.malos[i].pregunta_count+"</li>");
                };
                for(var i=0;i<data.buenos.length;i++){
                        $(".votainteligente .buenos ul").append("<li class=\"itemListadoCandidatos\">"+data.buenos[i].candidato+" ha respondido "+data.buenos[i].preguntas_respondidas+" de "+data.buenos[i].pregunta_count+"</li>");
                };
}
$(document).ready(function(){
        pintaElRanking();
});