<html>
    <head>
        <meta http-equiv="refresh" content="5">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Smart Health Tracking</title>
        <style>
            *{
                box-sizing: border-box;
            }
            .column {
                float : left;
                width : 33.33%;
                padding : 5px;
            }
            .row::after {
                content : "";
                display : table;
                clear : both;
            }
            body {
                background-image: linear-gradient(pink, orange, red);
            }
        </style>
    </head>
    <body>

        <?php
        $tot_content = file_get_contents("sensor_data.txt");
        $the_parts = explode("*",$tot_content);
        ?>

        <h1 style=" text-align: center;padding:0px 0px 10px 0px">Smart Health Tracking</h1>
        <div class ="row">
            <div class="column">
                <img src="https://img.freepik.com/free-vector/red-medical-heartbeat-line-vector-heart-shape-graphic-health-charity-concept_53876-111265.jpg?size=338&ext=jpg&ga=GA1.1.1395880969.1709164800&semt=ais" alt="Heart image" width="100%;" height="312px">
                <p style="text-align: center;">
                <table style="padding-left:110px;">
                    <tr>
                        <td><b>HEART RATE :  </b></td>
                        <td>  </td>
                        <td style="border:3px solid black;border-radius: 2px;padding:3px 42px">
                            <?php 
                                echo $the_parts_tmp[2]." bpm"; 
                            ?>
                        </td>
                    </tr>
                </table>
                </p>
            </div>
            <div class="column">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRZE3memj-hD2PT9I2bY6vwJDE1Fv-BKLk2w&usqp=CAU" alt="Temperature image" width="100%;" height="312px">
                <p style="text-align: center;">
                <table style="padding-left:110px;">
                    <tr>
                        <td><b>TEMPERATURE :  </b></td>
                        <td>  </td>
                        <td style="border:3px solid black;border-radius: 2px;padding:3px 39px">
                            <?php 
                                echo $the_parts_tmp[0]." degC"; 
                            ?>
                        </td>
                    </tr>
                </table>
                </p>
            </div>
            <div class="column">
                <img src="data:image/png;base64,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" alt="Humidity image" width="100%;" height="312px">
                <p style="text-align: center;">
                <table style="padding-left:110px;">
                    <tr>
                        <td><b>HUMIDITY : </b></td>
                        <td>  </td>
                        <td style="border:3px solid black;border-radius: 2px;padding:3px 42px">
                            <?php 
                                echo $the_parts_tmp[1]." g.m-3"; 
                            ?>
                        </td>
                    </tr>
                </table>
                </p>
            </div>
        </div>

        <table border="2px solid black">
            <caption>Axis Values</caption>
            <tr>
                <td  style="padding:4px">X-axis</td>
                <td  style="padding:4px"><?php echo $the_parts_tmp[3]." X"?></td>
            </tr>
            <tr>
                <td  style="padding:4px">Y-axis</td>
                <td  style="padding:4px"><?php echo $the_parts_tmp[4]." Y"?></td>
            </tr>
            <tr>
                <td  style="padding:4px">Z-axis</td>
                <td  style="padding:4px"><?php echo $the_parts_tmp[5]." Z"?></td>
            </tr>
        </table>
    </body>
</html>
