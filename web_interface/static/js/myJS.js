var theme = {
    color: [
        '#26B99A', '#8abb6f', '#BDC3C7', '#3498DB',
        '#9B59B6', '#34495E', '#759c6a', '#bfd3b7'
    ],

    title: {
        itemGap: 8,
        textStyle: {
            fontWeight: 'normal',
            color: '#408829'
        }
    },

    dataRange: {
        color: ['#1f610a', '#97b58d']
    },

    toolbox: {
        color: ['#408829', '#408829', '#408829', '#408829']
    },

    tooltip: {
        backgroundColor: 'rgba(0,0,0,0.5)',
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: '#408829',
                type: 'dashed'
            },
            crossStyle: {
                color: '#408829'
            },
            shadowStyle: {
                color: 'rgba(200,200,200,0.3)'
            }
        }
    },

    dataZoom: {
        dataBackgroundColor: '#eee',
        fillerColor: 'rgba(64,136,41,0.2)',
        handleColor: '#408829'
    },
    grid: {
        borderWidth: 0
    },

    categoryAxis: {
        axisLine: {
            lineStyle: {
                color: '#408829'
            }
        },
        splitLine: {
            lineStyle: {
                color: ['#eee']
            }
        }
    },

    valueAxis: {
        axisLine: {
            lineStyle: {
                color: '#408829'
            }
        },
        splitArea: {
            show: true,
            areaStyle: {
                color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
            }
        },
        splitLine: {
            lineStyle: {
                color: ['#eee']
            }
        }
    },
    timeline: {
        lineStyle: {
            color: '#408829'
        },
        controlStyle: {
            normal: {
                color: '#408829'
            },
            emphasis: {
                color: '#408829'
            }
        }
    },

    k: {
        itemStyle: {
            normal: {
                color: '#68a54a',
                color0: '#a9cba2',
                lineStyle: {
                    width: 1,
                    color: '#408829',
                    color0: '#86b379'
                }
            }
        }
    },
    map: {
        itemStyle: {
            normal: {
                areaStyle: {
                    color: '#ddd'
                },
                label: {
                    textStyle: {
                        color: '#c12e34'
                    }
                }
            },
            emphasis: {
                areaStyle: {
                    color: '#99d2dd'
                },
                label: {
                    textStyle: {
                        color: '#c12e34'
                    }
                }
            }
        }
    },
    force: {
        itemStyle: {
            normal: {
                linkStyle: {
                    strokeColor: '#408829'
                }
            }
        }
    },
    chord: {
        padding: 4,
        itemStyle: {
            normal: {
                lineStyle: {
                    width: 1,
                    color: 'rgba(128, 128, 128, 0.5)'
                },
                chordStyle: {
                    lineStyle: {
                        width: 1,
                        color: 'rgba(128, 128, 128, 0.5)'
                    }
                }
            },
            emphasis: {
                lineStyle: {
                    width: 1,
                    color: 'rgba(128, 128, 128, 0.5)'
                },
                chordStyle: {
                    lineStyle: {
                        width: 1,
                        color: 'rgba(128, 128, 128, 0.5)'
                    }
                }
            }
        }
    },
    gauge: {
        startAngle: 225,
        endAngle: -45,
        axisLine: {
            show: true,
            lineStyle: {
                color: [
                    [0.2, '#86b379'],
                    [0.8, '#68a54a'],
                    [1, '#408829']
                ],
                width: 8
            }
        },
        axisTick: {
            splitNumber: 10,
            length: 12,
            lineStyle: {
                color: 'auto'
            }
        },
        axisLabel: {
            textStyle: {
                color: 'auto'
            }
        },
        splitLine: {
            length: 18,
            lineStyle: {
                color: 'auto'
            }
        },
        pointer: {
            length: '90%',
            color: 'auto'
        },
        title: {
            textStyle: {
                color: '#333'
            }
        },
        detail: {
            textStyle: {
                color: 'auto'
            }
        }
    },
    textStyle: {
        fontFamily: 'Arial, Verdana, sans-serif'
    }
};
//var serverUrl = 'http://140.114.75.138:8080/data/';
var serverUrl = 'http://127.0.0.1:8080/data/';
var names = ['九層塔', '大蒜', '小白菜', '玉米', '地瓜', '竹筍', '辣椒',
                    '番茄', '花椰菜', '青江菜', '青蔥', '南瓜', '洋蔥', '甜椒',
                    '菠菜', '馬鈴薯', '高麗菜', '香蕉', '蘿蔔', '芒果', '草莓',
                    '葡萄', '西瓜', '鳳梨', '蘋果', '椪柑', '桃園', '宜蘭', '台中', '高雄', '台東'];
var echartLine;
var chartData = {
    name: '',
    type: 'line',
    smooth: true,
    itemStyle: {
        normal: {
            areaStyle: {
                type: 'default'
            }
        }
    },
    data: [10, 12, 21, 54, 43, 87, 34, 67, 77,87,99,100,105,134,64]
}

var predictData = {
    name: '預測',
    type: 'line',
    smooth: true,
    itemStyle: {
        normal: {
            areaStyle: {
                type: 'default'
            }
        }
    },
    data: [77,87,99,100,105,134,64]
};

Date.prototype.addDays = function(days) {
    var dat = new Date(this.valueOf())
    dat.setDate(dat.getDate() + days);
    return dat;
}

function getDates(startDate, stopDate) {
    var dateArray = new Array();
    var currentDate = startDate;
    while (currentDate <= stopDate) {
        dateArray.push( new Date (currentDate) )
        currentDate = currentDate.addDays(1);
    }
    dateArray = dateArray.map(function(date){
        var month = date.getMonth() + 1; //months from 1-12
        var day = date.getDate();
        var year = date.getFullYear();

        newdate = year + "/" + month + "/" + day;
        return newdate;
    });
    return dateArray;
}

function getData(){
    var product = $("#product_select option:selected").text();
    var location = $("#location_select option:selected").text();
    console.log(product + ' ' + location);
    $.getJSON(serverUrl, {product: product, location: location},
        function(data, textStatus) {
            console.log(data);
            chartData['name'] = data['product'];
            chartData['data'] = data['price'];
            var dates = getDates(new Date(data['starting_date']), new Date(data['ending_date']).addDays(7))
            predictData['data'] = [];
            for(var i = 0; i < 7; i++){
                predictData['data'].push(chartData['data'].pop());
            }
            for(var i = 0; i < 7; i++){
                chartData['data'].push(0);
            }
            if(predictData['data'].length < dates.length){
                var diff = dates.length - predictData['data'].length - 7;
                for(var i = 0; i < diff; i++){
                    predictData['data'].unshift(0);
                }
            }
            echartLine.setOption({
                legend: {
                    data: ['預測']
                },
                xAxis: [{
                    type: 'category',
                    boundaryGap: false,
                    data: dates
                }],
                series:[chartData, predictData]
            });
    });
}

$(document).ready(function() {
    echartLine = echarts.init(document.getElementById('echart_line'), theme);
    echartLine.setOption({
        title: {
            text: '歷史價格'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['高麗菜', '預測']
        },
        toolbox: {
            show: true,
            feature: {
                magicType: {
                    show: true,
                    ｉtitle: {
                        line: 'Line',
                        bar: 'Bar',
                        stack: 'Stack',
                    },
                    type: ['line', 'bar', 'stack']
                },
                restore: {
                    show: true,
                    title: "Restore"
                },
                saveAsImage: {
                    show: true,
                    title: "Save Image"
                }
            }
        },
        calculable: true,
        xAxis: [{
            type: 'category',
            boundaryGap: false,
            data: ['2016/5/1', '2016/5/2', '2016/5/3', '2016/5/4', '2016/5/5', '2016/5/6', '2016/5/7', '2016/5/8', '2016/5/9']
        }],
        yAxis: [{
            type: 'value'
        }],
        dataZoom: [{
            type: 'slider',
            start: 0,
            end: 100,
            xAxisIndex: 0
        }, {
            type: 'inside',
            start: 0,
            end: 100
        }],
        series: []
    });
    $('select').material_select();
    $('select').change(function(){getData();});
    getData();
});
