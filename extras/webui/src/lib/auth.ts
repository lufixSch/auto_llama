/** User authentication */
export class Authentication {
	private _secret: string | null = null;

	public login(secret: string) {
		this._secret = secret;
		localStorage.setItem('auth', secret);
	}

	public logout() {
		localStorage.removeItem('auth');
		this._secret = null;
	}

	public get secret() {
		return this._secret || localStorage.getItem('auth');
	}

	public get isAuthenticated() {
		return this.secret !== null;
	}
}

const auth = new Authentication();
export default auth;
