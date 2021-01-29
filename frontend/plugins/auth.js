export default ({ app, redirect, route }, inject) => {
	inject('authLogin', async (email, password, pin_code) => {
		return await app.$axios.post('/account/login/',
			{
				email: email,
				password: password,
				pin_code: pin_code
			}
		).then(resp => {
			app.store.commit('setUser', resp.data.user);
			app.$axios.setToken(resp.data.token, 'Bearer');
			app.$cookies.set('token', resp.data.token, {
				path: '/',
				maxAge: 60 * 60 * 24 * 7,
			});
			redirect('/exchange');

			// window.location.href = '/exchange/'; Что это?
			return true;
		}).catch(resp => {
		  return resp;
    })
	});
	inject('authLogout', () => {
		app.store.commit('deleteUser');
		app.$axios.setToken(null);
		app.$cookies.remove('token');
		window.location.href = '/'
	});
	inject('authFetchUser', async () => {
		let {data, status} = await app.$axios.get('/account/user/');
		if (status === 200) {
			app.store.commit('setUser', data)
		} else {
			redirect('/');
		}
	});
	inject('userIsLoggedIn', () => {
		return app.store.getters.user
	});
	inject('userIsStaff', () => {
		return app.store.getters.user && app.store.getters.user.is_staff
	});
	inject('userIsSuperuser', () => {
		if (app.store.getters.user) {
			return app.store.getters.user.is_superuser
		}
		return false
	});
}
