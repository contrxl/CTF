# Outcast
From main page, a quick look at the source code reveals the following comment:
```html
<!-- note: should not be accessable -->
<!-- <a href="/test" class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white">Test</a> -->
```
Hitting the `/test` endpoint reveals an API caller. Template code can be downloaded for this (apitemplate.txt). The template code does not perform any input sanitisation. Notably:
```JavaScript
foreach($data as $k -> & $v)
	if (($v) && (is_string($v)) && str_starts_with($v, '@')) {
		$file = substr($v, 1);
		if (str_starts_with($file, $this - > path_tmp)) {
			$v = file_get_contents($file);
		}
	}
```
This checks if the input given (`$v`) begins with the '@' symbol, if it does, it takes it as a substring and tries to get the contents of that path. So if you gave it `@/tmp/../etc/passwd`, it would perform `file_get_contents` without any checks. However, the only output we get when trying this is:
```html
{"status":"OK"}
```
If we call the login page using the API method with:
```html
../login/
```
We see the parameters it require: `username` and `password`. Note that the `../` is required because the API is calling from inside `/modules` by default (this can be seen in source code on line 126). The preceding `/` is needed because otherwise the method returns a `301 Moved Permanently"`.
```html
<p>The document has moved <a http://localhost:8080/login/">here</a>.</p>
```
Now we can combine these, using `../login/` as the module and `username=@/tmp/../etc/passwd` we can see the actual file written out in the HTML output! To get the flag, simply change the parameter to `username=@/tmp/../flag.txt`.
