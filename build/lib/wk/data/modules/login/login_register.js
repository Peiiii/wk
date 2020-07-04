const loginUtils = (function () {
    const checkPhoneNumber = function (el) {
        let phone = $(el).val();
        if (!utils.isMobileNumber(phone)) {
            $.jGrowl('请输入正确的电话号码');
            return false;
        }
        return true;
    };
    const checkEmailFormat = function (el) {
        let email = $(el).val();
        if (!utils.isValidEmail(email)) {
            $.jGrowl('请输入正确的邮箱地址');
            return false;
        }
        return true;
    };
    const checkPassword = function (el1, el2 = null) {
        el1 = $(el1);
        let flag;

        function checkOnce(el) {
            let flag = true;
            if (!utils.isValidPassword(el.val())) {
                $.jGrowl('密码必须由 4-16位字母、数字、特殊符号线组成');
                console.log("password got:", el.val());
                flag = false;
            }
            return flag;
        }

        flag = checkOnce(el1);
        if (el2) {
            el2 = $(el2);
            if (el1.val() !== el2.val()) flag = false;
        }
        return flag;
    };

    const loadAccessToken = function () {
    };
    const sendSmsCode = function (phoneNumber, callback) {
        if (!utils.isMobileNumber(phoneNumber)) {
            $.jGrowl('电话号码错误');
            return null;
        }
        let data = {target: phoneNumber};
        return utils.postJSON(CONFIG.URL.sendSmsCode, data, (e) => {
            if (callback) callback(e);
        });
    };
    const sendEmailCode = function (email, callback) {
        if (!utils.isValidEmail(email)) {
            $.jGrowl('邮箱地址错误');
            return null;
        }
        let data = {target: email};
        return utils.postJSON(CONFIG.URL.sendEmailCode, data, (e) => {
            if (callback) callback(e);
        });
    };
    return {
        checkEmailFormat,
        checkPassword,
        checkPhoneNumber,
        loadAccessToken,
        sendEmailCode,
        sendSmsCode,
    }
})();
