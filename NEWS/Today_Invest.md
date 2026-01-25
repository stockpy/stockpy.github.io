<center>Vers : 20260125_0827 </center>
<center>Vers : 20260125_1727 </center>
<br>
<style type="text/css"> .tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-0lax{text-align:left;vertical-align:top}
</style>
<center>
<link rel="stylesheet" href="https://naver.github.io/billboard.js/release/latest/dist/theme/datalab.min.css">
<script src="https://naver.github.io/billboard.js/release/latest/dist/billboard.pkgd.min.js"></script>
<div id="barChart"></div>
<table border="1" class="dataframe tg">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ETF_Name</th>
      <th>Alloc_P</th>
      <th>Price</th>
      <th>CALL</th>
      <th>MY_PERC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>KODEX 200TR</td>
      <td>0%</td>
      <td>26240</td>
      <td>0</td>
      <td>0%</td>
    </tr>
    <tr>
      <th>1</th>
      <td>KODEX 미국S&amp;P500</td>
      <td>50%</td>
      <td>23130</td>
      <td>12</td>
      <td>56.0%</td>
    </tr>
    <tr>
      <th>2</th>
      <td>KODEX iShares미국투자등급회사채액티브</td>
      <td>15%</td>
      <td>12025</td>
      <td>7</td>
      <td>11.0%</td>
    </tr>
    <tr>
      <th>3</th>
      <td>KODEX 미국10년국채선물</td>
      <td>10%</td>
      <td>12410</td>
      <td>4</td>
      <td>15.0%</td>
    </tr>
    <tr>
      <th>4</th>
      <td>KODEX 미국30년국채액티브(H)</td>
      <td>10%</td>
      <td>8885</td>
      <td>6</td>
      <td>7.0%</td>
    </tr>
    <tr>
      <th>5</th>
      <td>KODEX 미국배당다우존스</td>
      <td>15%</td>
      <td>11715</td>
      <td>7</td>
      <td>11.0%</td>
    </tr>
    <tr>
      <th>6</th>
      <td>TIGER 미국필라델피아반도체나스닥</td>
      <td>0%</td>
      <td>31000</td>
      <td>0</td>
      <td>0%</td>
    </tr>
    <tr>
      <th>7</th>
      <td>ACE 테슬라밸류체인액티브</td>
      <td>0%</td>
      <td>22700</td>
      <td>0</td>
      <td>0%</td>
    </tr>
  </tbody>
</table><br>
<script>
var chart = bb.generate({
data: {
columns: [
['KODEX 미국S&P500', '56.0'],
['KODEX iShares미국투자등급회사채액티브', '11.0'],
['KODEX 미국10년국채선물', '15.0'],
['KODEX 미국30년국채액티브(H)', '7.0'],
['KODEX 미국배당다우존스', '11.0']
],
type: "pie", // for ESM specify as: pie()
},
pie: {
expand: {
rate: 1.007
}
},
bindto: "#expandRate"
});
</script>
</center>
