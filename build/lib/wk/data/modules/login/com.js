const com = (function () {
    const ActionLib = {
        redirect: function (params, resp) {
            let target = params.target || params.href || params.url || params.location;
            $.jGrowl(`即将跳转至<a href="${target}">${target}</a>`);
            setTimeout(() => {
                window.location.href = target;
            }, 1000);
        },
        checkStatus: function (resp) {
            if (resp.message) {
                this.showMessage(resp.message);
            }
            return !!this.success;
        },
        showMessage: function (message) {
            $.jGrowl(message);
        }
    };
    const checkResponse = function (resp) {
        if (resp.action) {
            let action = ActionLib[resp.action];
            return action(resp.params, resp);
        } else {
            let action = ActionLib.checkStatus(resp);
            return action(resp);
        }
    };

    return {
        checkResponse, ActionLib,
    };
})();
