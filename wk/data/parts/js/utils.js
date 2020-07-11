const utils = (function () {
    function isMobileNumber(phone) {
        var flag = false;
        var message = "";
        var myreg = /^(((13[0-9]{1})|(14[0-9]{1})|(17[0-9]{1})|(15[0-3]{1})|(15[4-9]{1})|(18[0-9]{1})|(199))+\d{8})$/;
        if (phone === '') {
            // console.log("手机号码不能为空");
            message = "手机号码不能为空！";
        } else if (phone.length !== 11) {
            //console.log("请输入11位手机号码！");
            message = "请输入11位手机号码！";
        } else if (!myreg.test(phone)) {
            //console.log("请输入有效的手机号码！");
            message = "请输入有效的手机号码！";
        } else {
            flag = true;
        }
        if (message !== "") {
            // alert(message);
        }
        return flag;
    }

    const isValidEmail = function (email) {
        let emreg = /^\w{3,}(\.\w+)*@[A-z0-9]+(\.[A-z]{2,5}){1,2}$/;
        return emreg.test(email);
    };
    const isValidPassword = function (text) {
        const reg = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[~!@#$%^&*()_+`\-={}:";'<>?,.\/]).{4,16}$/;
        return reg.test(text);
    };
    const renderToggleShowPassword = function () {
        let toggles = $('[data-toggle=show-password]');
        $.each(toggles, (i, toggle) => {
            toggle = $(toggle);
            let target = $(toggle.attr('data-target'));
            let btn_show = toggle.find('.toggle-show');
            let btn_hide = toggle.find('.toggle-hide');

            function init() {
                let type = target.attr('type');
                if (type === 'password') {
                    btn_show.show();
                    btn_hide.hide();
                } else {
                    btn_show.hide();
                    btn_hide.show();
                }
            }

            init();

            toggle.click(() => {
                let type = target.attr('type');
                if (type ==='password') {
                    target.attr('type', 'text');
                    btn_show.hide();
                    btn_hide.show();
                } else {
                    target.attr('type', 'password');
                    btn_show.show();
                    btn_hide.hide();
                }
            })
        })
    };
    const getCodeSendTimerCallback = function (el) {
        el = $(el);
        let send_btn = el.find('.btn-before');
        let info_btn = el.find('.btn-after');

        function disable(count) {
            send_btn.addClass('d-none');
            info_btn.removeClass('d-none');
            info_btn.text(`${count}秒后可重新发送`);
        }

        function recover() {
            info_btn.addClass('d-none');
            send_btn.removeClass('d-none');
        }

        callback = function () {

            let count = 60;
            disable(count);

            function setTime() {
                if (count === 0) {
                    recover();
                } else {
                    count--;
                    disable(count);
                    setTimeout(() => {
                        setTime();
                    }, 1000);
                }
            }

            setTime();
        };
        // el.click(callback);
        return callback;
    };
    const gatherFormDataAsJSON = function (el) {
        el = $(el);
        var unindexed_array = el.serializeArray();
        var indexed_array = {};
        $.map(unindexed_array, function (n, i) {
            indexed_array[n['name']] = n['value'];
        });
        return indexed_array;
    };
    const postJSON = function (url, data, success) {
        $.post({
            url: url,
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: (e) => {
                if (success) success(e);
            }
        })
    };


    const renderAll = function () {
        renderToggleShowPassword();
    };
    return {
        isMobileNumber,
        isValidEmail,
        isValidPassword,
        renderToggleShowPassword,
        getCodeSendTimerCallback,
        gatherFormDataAsJSON,
        postJSON,
        renderAll
    };
})
();
