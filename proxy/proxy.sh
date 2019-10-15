export GRADLE_OPTS="-Dhttp.proxyUrl=http://proxy.sei.cmu.edu -Dhttp.proxyPort=8080 -Dhttps.proxyUrl=http://proxy.sei.cmu.edu -Dhttps.proxyPort=8080"
# NOTE: this is only needed if behind a proxy.
PROXY="http://proxy.sei.cmu.edu:8080"
#echo "Acquire::http::Proxy \"${PROXY}\";" | sudo tee /etc/apt/apt.conf

# NOTE: this is only needed if behind a proxy.
export http_proxy=${PROXY}
export https_proxy=${PROXY}
export HTTP_PROXY=${PROXY} 
export HTTPS_PROXY=${PROXY}

