---
layout: post
title:  Comparing Effective Salaries in Different Regions
date:   2016-04-30
categories: [Tools]
tags: [tool, finances]
excerpt_separator: <!--more-->
---

While job hunting, I wanted a way to compare offers that could take different cost of living and tax rates into account.
Hacked this thing up.
<!--more-->
It has hardcoded 2015 tax brackets pulled from <a href="http://www.tax-brackets.org">tax-brackets.org</a> - it is not super accurate but should give a kind of rough idea of how salaries actually compare.

I assume the user is single and has no dependants or other investments. Things are a little messier when those assumptions go away.

This will save your session locally, but does not send any data to a server (in fact, davidbstein.com is a static stite)
    
<script type="text/javascript" charset="utf-8" src="/static/external/jquery.js"></script>

<script>

  window.onload = (function(){
    $("#the-chart").html("");

    var FEDERAL_BRACKETS = [
      [0, .1],
      [9225, .15],
      [37450, .25],
      [90750, .28],
      [189300, .33],
      [411500, .35],
      [413200, .396]
    ];
    // see tax_chart.json
    var STATE_BRACKETS = {
    "Alabama":[[0,0.02],[500,0.04],[3000,0.06]],
    "Alaska":[[0,0]],
    "Arizona":[[0,0.0259],[10000,0.0288],[25000,0.0336],[50000,0.0424],[150000,0.0454]],
    "Arkansas":[[0,0.01],[3900,0.025],[7800,0.035],[11700,0.045],[19600,0.06],[32600,0.07]],
    "California":[[0,0.01],[7124,0.02],[16890,0.04],[26657,0.06],[37005,0.08],[46766,0.093],[1000000,0.103]],
    "Colorado":[[0,0.0463]],
    "Connecticut":[[0,0.03],[10000,0.05],[500000,0.065]],
    "Delaware":[[2000,0.022],[5000,0.039],[10000,0.048],[20000,0.052],[25000,0.0555],[60000,0.0695]],
    "District Of Columbia":[[0,0.04],[10000,0.06],[40000,0.06]],
    "Florida":[[0,0]],
    "Georgia":[[0,0.01],[750,0.02],[2250,0.03],[3750,0.04],[5250,0.05],[7000,0.06]],
    "Hawaii":[[0,0.014],[2400,0.032],[4800,0.055],[9600,0.064],[14400,0.068],[19200,0.072],[24000,0.076],[36000,0.079],[48000,0.0825],[150000,0.09],[175000,0.1],[300000,0.11]],
    "Idaho":[[0,0.016],[1323,0.036],[2642,0.042],[3963,0.051],[5284,0.062],[6604,0.071],[9907,0.074],[26418,0.078]],
    "Illinois":[[0,0.05]],
    "Indiana":[[0,0.034]],
    "Iowa":[[0,0.003],[1439,0.0058],[2878,0.0243],[5756,0.045],[12951,0.0612],[21585,0.0648],[28780,0.068],[43170,0.0792],[64755,0.0898]],
    "Kansas":[[0,0.035],[15000,0.0625],[30000,0.0645]],
    "Kentucky":[[0,0.02],[3000,0.03],[4000,0.04],[5000,0.05],[8000,0.058],[75000,0.06]],
    "Louisiana":[[0,0.02],[12500,0.04],[50000,0.06]],
    "Maine":[[0,0.02],[5000,0.045],[9950,0.07],[19950,0.085]],
    "Maryland":[[0,0.02],[1000,0.03],[2000,0.04],[3000,0.0475],[150000,0.05],[300000,0.0525],[500000,0.055]],
    "Massachusetts":[[0,0.053]],
    "Michigan":[[0,0.0435]],
    "Minnesota":[[0,0.0535],[23100,0.0705],[75891,0.0795]],
    "Mississippi":[[0,0.03],[5000,0.04],[10000,0.05]],
    "Missouri":[[0,0.015],[1000,0.02],[2000,0.025],[3000,0.03],[4000,0.035],[5000,0.04],[6000,0.045],[7000,0.05],[8000,0.055],[9000,0.06]],
    "Montana":[[0,0.01],[2600,0.02],[4600,0.03],[6900,0.04],[9400,0.05],[12100,0.06],[15600,0.069]],
    "Nebraska":[[0,0.0256],[2400,0.0357],[17500,0.0512],[27000,0.0684]],
    "Nevada":[[0,0]],
    "New Hampshire":[[0,0.05]],
    "New Jersey":[[0,0.014],[20000,0.0175],[35000,0.035],[0,0.0553],[75000,0.0637],[500000,0.0897]],
    "New Mexico":[[0,0.017],[5500,0.032],[11000,0.047],[16000,0.049]],
    "New York":[[0,0.04],[8000,0.045],[11000,0.0525],[13000,0.059],[20000,0.0685],[200000,0.0785],[500000,0.0897]],
    "North Carolina":[[0,0.06],[12750,0.07],[60000,0.0775]],
    "North Dakota":[[0,0.0184],[34000,0.0344],[82400,0.0381],[171850,0.0442],[373650,0.0486]],
    "Ohio":[[0,0.0059],[0,0.0117],[0,0.0235],[0,0.0294],[0,0.0352],[0,0.0411],[0,0.047],[0,0.0545],[0,0.0592]],
    "Oklahoma":[[0,0.004],[1000,0.01],[2500,0.02],[3750,0.03],[4900,0.04],[7200,0.05],[8700,0.055]],
    "Oregon":[[0,0.05],[3100,0.07],[7750,0.09],[125000,0.108],[250000,0.11]],
    "Pennsylvania":[[0,0.03]],
    "Rhode Island":[[0,0.0375],[55000,0.0475],[125000,0.0599]],
    "South Carolina":[[0,0],[2760,0.03],[5520,0.04],[8280,0.05],[11040,0.06],[13800,0.07]],
    "South Dakota":[[0,0]],
    "Tennessee":[[0,0.06]],
    "Texas":[[0,0]],
    "Utah":[[0,0.05]],
    "Vermont":[[0,0.0355],[34500,0.068],[83600,0.078],[174400,0.088],[379150,0.0895]],
    "Virginia":[[0,0.02],[3000,0.03],[5000,0.05],[17000,0.0575]],
    "Washington":[[0,0]],
    "West Virginia":[[10000,0.04],[0,0.03],[25000,0.045],[40000,0.06],[60000,0.065]],
    "Wisconsin":[[0,0.046],[10180,0.0615],[20360,0.065],[152740,0.0675],[224210,0.0775]],
    "Wyoming":[[0,0]],
    "none":[[0, 0]]
      };
    var CITY_BRACKETS = {
      "NYC": [
        [0, .02907],
        [21600, .03534],
        [45000, .03591],
        [90000, .03648],
        [500000, .03876]
      ]
    };
    var CITY_STATES = {
      NYC: "New York"
    }

    var STORE_KEY_ENTRIES = "salaray-entries"
    var STORE_KEY_CONFIG = "salaray-config"

    var SalaryChart = {}

    var entries, config;
    try {
      entries = JSON.parse(window.localStorage.getItem(STORE_KEY_ENTRIES)) || [];
    } catch(e) {
      entries = [];
    }

    try {
      config = JSON.parse(window.localStorage.getItem(STORE_KEY_CONFIG)) || {max_401k: false};
      $("input[name=max_401k]")[0].checked = config.max_401k;
    } catch(e) {
      config = {
        max_401k: $("input[name=max_401k]")[0].checked
      }
    }

    function save_state(){
      localStorage.setItem(STORE_KEY_ENTRIES, JSON.stringify(entries))
      localStorage.setItem(STORE_KEY_CONFIG, JSON.stringify(config))
    }

    function read_new_entry(args){
      var entry = {};
      var process_fns = [
        ["label", function(v){return v || "(no name set)";}],
        ["salary", function(v){return parseFloat(v) || 0;}],
        ["bonus", function(v){return parseFloat(v) || 0;}],
        ["rent", function(v){return parseFloat(v) || 0;}],
        ["costs", function(v){return parseFloat(v) || 0;}],
        ["savings", function(v){return parseFloat(v) || 0;}],
        ["match_401k", function(v){return parseFloat(v) || 0;}],
        ["perks", function(v){return parseFloat(v) || 0;}],
        ["location", function(v){return v || "none";}]
      ];
      $(".new-entry input").each(function(i, field){
        entry[field.name] = field.value;
      });
      $(".new-entry select").each(function(i, field){
        entry[field.name] = field.value;
      });
      process_fns.map(function(e){
        var k = e[0]; var fn = e[1];
        entry[k] = fn(entry[k]);
      })
      return entry
    }

    function compute_tax(entry, brackets){
      var income = entry.salary - (config.max_401k ? 18000 : 0);
      var tax = 0;
      brackets.map(function(b, idx){
        var next = brackets[idx+1];
        return [b[0], next ? next[0] : Math.max(income, b[0]), b[1]];
      }).forEach(function(bracket){
        var min = Math.min(bracket[0], income);
        var max = Math.min(bracket[1], income);
        tax += (max - min) * bracket[2];
      });
      return tax;
    }

    function compute_breakdown(entry){
      var state = entry.location;
      var amounts = {};
      amounts.city_tax = 0
      if (!STATE_BRACKETS[state]) {
        state = CITY_STATES[entry.location];
        amounts.city_tax = compute_tax(entry, CITY_BRACKETS[entry.location]);
      }
      amounts.state_tax = compute_tax(entry, STATE_BRACKETS[state]);
      amounts.federal_tax = compute_tax(entry, FEDERAL_BRACKETS);
      amounts.rent = entry.rent * 12;
      amounts.retirement = config.max_401k ? entry.match_401k + 18000 : 0;
      amounts.perks = entry.perks;
      amounts.costs = entry.costs * 12;
      amounts.bonus = entry.bonus;
      amounts.surplus = ( entry.salary
        - amounts.costs
        - amounts.city_tax
        - amounts.state_tax
        - amounts.federal_tax
        - amounts.rent
        - amounts.retirement
      );
      return amounts
    }

    function format_amount(amount, label){
      var labelstr = label ? label + " - " : "";
      var formatted = labelstr + "$" + amount.toLocaleString()
      return $("<span>").text(formatted);
    }

    var _leftfields = ['city_tax', 'state_tax', 'federal_tax', 'rent', 'costs'];
    var _rightfields = ['retirement', 'surplus', 'bonus', 'perks'];

    function draw_entry_bar(breakdown, scale){
      if (breakdown.surplus < 0 || scale <= 0){
        return {
          bar: $("<div>", {"class": "unlivable-bar"}).text("unlivable"),
          leftscale: 100,
          rightscale: 100
        }
      }


      var leftscale = _leftfields.reduce(function(prevVal, cur){
        return prevVal + (breakdown[cur] / scale)
      }, 0)
      var lefttotal = _leftfields.reduce(function(prevVal, cur){
        return prevVal + breakdown[cur]
      }, 0)
      var leftbar = $("<div class='leftbar'>")
        .attr("style", "width:" + (100 * leftscale) + "%")
        .append(format_amount(lefttotal).attr({"class": "biglabel"}));
      _leftfields.forEach(function(field){
        leftbar.append(
          $("<div>", {"class": field, "style":"width:" + (100 * breakdown[field] / (scale * leftscale) ) + "%"})
          .append(format_amount(breakdown[field], field))
        );
      })


      var rightscale = _rightfields.reduce(function(prevVal, cur){
        return prevVal + (breakdown[cur] / scale)
      }, 0)
      var righttotal = _rightfields.reduce(function(prevVal, cur){
        return prevVal + breakdown[cur]
      }, 0)
      var rightbar = $("<div class='rightbar'>")
        .attr("style", "width:" + (100 * rightscale) + "%")
        .append(format_amount(righttotal).attr({"class": "biglabel"}));
      _rightfields.forEach(function(field){
        rightbar.append(
          $("<div>", {"class": field, "style":"width:" + (100 * breakdown[field] / (scale * rightscale) ) + "%"})
          .append(format_amount(breakdown[field], field))
        );
      })
      return {
        bar: $("<div>", {"class": "bar"}).append(leftbar).append(rightbar),
        leftscale: leftscale,
        rightscale: rightscale
      }
    }

    function redraw(){
      var new_chart = $("<div id='the-chart' class='chart'>");
      var scale = 1.3 * entries.reduce(
        function(prev, cur){
          return Math.max(prev, cur.salary + cur.bonus)
        },
        0
      );
      var bars = entries.map(function(e){
        var to_ret = draw_entry_bar(compute_breakdown(e), scale);
        to_ret.entry = e;
        return to_ret;
      });
      var max_left_scale = bars.reduce(function(prevVal, cur){return Math.max(prevVal, cur.leftscale);}, 0.5);
      bars.forEach(function(b, idx){
        new_chart.append($("<div>").text(b.entry.label));
        new_chart.append($("<button onclick='SalaryChart.remove_entry("+idx+")'>").text("remove"));
        new_chart.append($("<div>"));
        buffersize = 100 * (max_left_scale - b.leftscale);
        new_chart.append(b.bar.prepend($("<div>", {class: "leftbuff", style: "width:" + buffersize + "%"})));
      })
      $("#the-chart").html(new_chart.html());
    }

    SalaryChart.clear_entry_input = function(){
      $(".new-entry input").each(function(i, field){
        $(field).val("");
      })
      $(".new-entry select").val("");
    }

    SalaryChart.update = function(){
      config.max_401k = $("input[name=max_401k]")[0].checked;
      save_state();
      redraw();
    }

    SalaryChart.add_entry = function(){
      var entry = read_new_entry();
      entries.push(entry);
      save_state();
      redraw();
    }

    SalaryChart.remove_entry = function(idx){
      entries = entries.slice(0,idx).concat(entries.slice(idx+1));
      save_state();
      redraw();
    }

    window.SalaryChart = SalaryChart;
    redraw();


    function draw_key(){
      var key = $("<div id='the-key'>");
      function drawfunc(fieldname){
        return $("<div>")
          .append($("<span>", {class: fieldname + " labeldiv"}))
          .append("<span>" + fieldname + "</div>")
      }
      var leftdiv = $("<div>")
      _leftfields.map(drawfunc).forEach(function(item){leftdiv.append(item)});
      key.append(leftdiv)
      var rightdiv = $("<div>")
      _rightfields.map(drawfunc).forEach(function(item){rightdiv.append(item)});
      key.append(rightdiv)
      $("#the-key").html(key.html());
    }
    draw_key();
  })
</script>
<style>
  div#the-key {
    border: 1px solid #ccc;
    margin: 8px;
  }
  .labeldiv {
    width: 16px;
    height: 16px;
    display: inline-block;
  }
  #the-key div {
    display: inline-block;
    margin: 2px 8px;
  }
  #the-key span {
    margin: 0px 4px;
  }
  div#the-chart {
    margin: 8px;
    border: 1px solid #ccc;
    padding: 8px;
  }
  span.biglabel {
    color: transparent;
    position: absolute;
    margin-top: -28px;
    cursor: default;
  }
  .bar:hover span.biglabel {
    color: black
  }
  .entry-header {
    margin-top: 16px;
  }
  .bar div div {
    cursor: default;
    display: inline-block;
    color: transparent;
    margin: 0;
    white-space: nowrap;
  }
  .bar div div:hover span {
    color: black;
    overflow: visible;
    display: inline-block;
    position: relative;
    top: 22px;
  }

  .bar .leftbar, .bar .rightbar {
    display: inline;
    margin-bottom: 25px;
    padding-top: 8px;
  }

  .leftbar {
    background: #fbb;
  }

  .rightbar {
    background: #bef;
  }

  .city_tax {
    background: red;
  }

  .leftbuff {
    height: 1px;
  }

  .state_tax {
    background: #FF8D00;
  }

  .federal_tax {
    background: #FFD400;
  }

  .rent {
    background: #FB06FB;
  }

  .costs {
    background: maroon;
  }

  .retirement {
    background: blue;
  }

  .surplus {
    background: #00D860;
  }

  .bonus {
    background: #15FFFF;
  }

  .perks {
    background: #3FBDEC;
  }

  .unlivable-bar {
    background: #ccc;
    text-align: center;
    width: 400px;
    margin: auto;
  }

  .bar {
    padding-top:25px;
    height: 50px;
    display: flex;
  }
</style>
<div id="content-wrapper">
  <div id="content-wrapper-bg"></div>
  <div id="content-wrapper-fg" class="text-document">
    <div>
      <div  >
        <div  >
          <h2  >
            <span  >Add new offer</span>
          </h2>
          <div class="new-entry">
            <div class="entry-header"> Basics </div>
            <input placeholder="Job Name" name="label"/>
            <input placeholder="Annual Salary" name="salary" type="number"/>
            <input placeholder="Bonus" name="bonus" type="number"/>
            <select placeholder="Location" name="location">
              <option value="">--- Location</option>
              <option value="NYC">New York City</option>
              <option value="Alabama"> Alabama </option>
              <option value="Alaska"> Alaska </option>
              <option value="Arizona"> Arizona </option>
              <option value="Arkansas"> Arkansas </option>
              <option value="California"> California </option>
              <option value="Colorado"> Colorado </option>
              <option value="Connecticut"> Connecticut </option>
              <option value="Delaware"> Delaware </option>
              <option value="District Of Columbia"> District Of Columbia </option>
              <option value="Florida"> Florida </option>
              <option value="Georgia"> Georgia </option>
              <option value="Hawaii"> Hawaii </option>
              <option value="Idaho"> Idaho </option>
              <option value="Illinois"> Illinois </option>
              <option value="Indiana"> Indiana </option>
              <option value="Iowa"> Iowa </option>
              <option value="Kansas"> Kansas </option>
              <option value="Kentucky"> Kentucky </option>
              <option value="Louisiana"> Louisiana </option>
              <option value="Maine"> Maine </option>
              <option value="Maryland"> Maryland </option>
              <option value="Massachusetts"> Massachusetts </option>
              <option value="Michigan"> Michigan </option>
              <option value="Minnesota"> Minnesota </option>
              <option value="Mississippi"> Mississippi </option>
              <option value="Missouri"> Missouri </option>
              <option value="Montana"> Montana </option>
              <option value="Nebraska"> Nebraska </option>
              <option value="Nevada"> Nevada </option>
              <option value="New Hampshire"> New Hampshire </option>
              <option value="New Jersey"> New Jersey </option>
              <option value="New Mexico"> New Mexico </option>
              <option value="New York"> New York </option>
              <option value="North Carolina"> North Carolina </option>
              <option value="North Dakota"> North Dakota </option>
              <option value="Ohio"> Ohio </option>
              <option value="Oklahoma"> Oklahoma </option>
              <option value="Oregon"> Oregon </option>
              <option value="Pennsylvania"> Pennsylvania </option>
              <option value="Rhode Island"> Rhode Island </option>
              <option value="South Carolina"> South Carolina </option>
              <option value="South Dakota"> South Dakota </option>
              <option value="Tennessee"> Tennessee </option>
              <option value="Texas"> Texas </option>
              <option value="Utah"> Utah </option>
              <option value="Vermont"> Vermont </option>
              <option value="Virginia"> Virginia </option>
              <option value="Washington"> Washington </option>
              <option value="West Virginia"> West Virginia </option>
              <option value="Wisconsin"> Wisconsin </option>
              <option value="Wyoming"> Wyoming </option>
            </select>
            <div class="entry-header"> Monthly Costs (optional) </div>
            <input placeholder="Monthly Rent" name="rent" type="number"/>
            <input placeholder="Monthly Costs" name="costs" type="number"/>
            <div class="entry-header"> Perks (optional) </div>
            <input placeholder="401k matching" name="match_401k" type="number"/>
            <input placeholder="value of other perks" name="perks" type="number"/>
            <div style="margin-top:32px">
              <button onclick="SalaryChart.add_entry()"> Add new entry </button>
              <button onclick="SalaryChart.clear_entry_input()"> clear </button>
            </div>
          </div>
          <h2  >
            <span  >Comparison</span>
          </h2>
          <div id='the-key'>key</div>
          <div class="chart" id="the-chart">
            (loading chart...)
          </div>
          <div><label><input name="max_401k" type="checkbox" onclick="SalaryChart.update()" />I will max out my 401k</label></div>
        </div>
      </div>
    </div>
  </div>
</div>