<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>
      Kaarsemaker.net - Home 
    </title>
    <link rel="stylesheet" type="text/css" href="/static/css/kaarsemaker.css"/>
    <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon" />
    <script type="text/javascript" src="/static/js/mootools.js"></script>
    <script type="text/javascript" src="/static/js/mootools-plugins.js"></script>
    <script type="text/javascript" src="/static/js/base.js"></script>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="keywords" content="dennis, kaarsemaker" />
    <meta name="description" content="De homepage van Dennis Kaarsemaker" />
    <meta name="author" content="Dennis Kaarsemaker" />
    <meta name="robots" content="index,follow" />
    
  <link rel="stylesheet" type="text/css" href="/static/css/filebrowse.css"/>
  <script type="text/javascript" src="/static/js/filebrowse.js"></script>

  </head>
  <body id="body_home">
    <div id="site">

      <div id="outer_head">
        <div id="inner_head">
          <div id="left_buttons">
          </div>
          <div id="right_buttons">
          </div>
        </div>
      </div>

      <div id="sitecontent">
        
        
<table id="filebrowser" border="0">
  <tr><td colspan="3" id="pathbar">Browsing <span id="browsepath">/code/django/</span></td></tr>
  <tr>
    <td id="treepanel" rowspan="2"><ul id="browsetree"><li id="folder_/downloads/code/"><a href="/downloads/code/" onclick="return go($(this).get('href'))"><img src="http://www.kaarsemaker.net/static/images/Tango/16x16/places/folder.png">code</a><ul><li id="folder_/downloads/code/nagios/"><a href="/downloads/code/nagios/" onclick="return go($(this).get('href'))"><img src="http://www.kaarsemaker.net/static/images/Tango/16x16/places/folder.png">nagios</a><ul></ul></li><li id="folder_/downloads/code/django/"><a href="/downloads/code/django/" onclick="return go($(this).get('href'))"><img src="http://www.kaarsemaker.net/static/images/Tango/16x16/places/folder.png">django</a><ul></ul></li></ul></li><li id="folder_/downloads/pictures/"><a href="/downloads/pictures/" onclick="return go($(this).get('href'))"><img src="http://www.kaarsemaker.net/static/images/Tango/16x16/places/folder.png">pictures</a><ul></ul></li><li id="folder_/downloads/ubuntu/"><a href="/downloads/ubuntu/" onclick="return go($(this).get('href'))"><img src="http://www.kaarsemaker.net/static/images/Tango/16x16/places/folder.png">ubuntu</a><ul></ul></li></ul></td>
    <td colspan="2" id="browsenav"><a href="/downloads/" onclick="return go(this.get('href'))"><img src="http://www.kaarsemaker.net/static/images/Tango/16x16/actions/go-home.png"> Home</a><a href="/downloads/code/django/" onclick="return go(this.get('href'))"><img src="http://www.kaarsemaker.net/static/images/Tango/16x16/actions/go-up.png"> Up</a><a href="/downloads/code/django/filtercache.py" onclick="return go(this.get('href'))"><img src="http://www.kaarsemaker.net/static/images/Tango/16x16/actions/go-previous.png"> Previous</a><a href="/downloads/code/django/query.py" onclick="return go(this.get('href'))"> Next <img src="http://www.kaarsemaker.net/static/images/Tango/16x16/actions/go-next.png"></a><a href="http://www.kaarsemaker.net/static/downloads/code/django/hosturl.py" onclick="window.open('http://www.kaarsemaker.net/static/downloads/code/django/hosturl.py'); return false"><img src="http://www.kaarsemaker.net/static/images/Tango/16x16/actions/document-save.png"> Download</a></td>
  </tr>
  <tr>
    <td id="metapanel"><div id="browsemeta">
      <img src="http://www.kaarsemaker.net/static/images/Tango/32x32/mimetypes/gnome-mime-text-x-python.png" /><br />
        hosturl.py<br />
        3.75 KB<br />
      <p>
        
        103 lines<br />
        
      </p>
    </div></td>
    <td id="datapanel"><div id="browsedata">
        <div class="highlight"><pre><span class="lineno">  1</span> <span class="c"># Modified version of the {% url %} tag that allows you to specify a hostname</span>
<span class="lineno">  2</span> <span class="c"># {% hosturl http://hostpath/path path.to.some_view arg1,arg2,name1=value1 %}</span>
<span class="lineno">  3</span> 
<span class="lineno">  4</span> <span class="k">from</span> <span class="nn">django</span> <span class="k">import</span> <span class="n">template</span>
<span class="lineno">  5</span> <span class="k">from</span> <span class="nn">django.conf</span> <span class="k">import</span> <span class="n">settings</span>
<span class="lineno">  6</span> 
<span class="lineno">  7</span> <span class="n">register</span> <span class="o">=</span> <span class="n">template</span><span class="o">.</span><span class="n">Library</span><span class="p">()</span>
<span class="lineno">  8</span> 
<span class="lineno">  9</span> <span class="k">class</span> <span class="nc">HostURLNode</span><span class="p">(</span><span class="n">template</span><span class="o">.</span><span class="n">Node</span><span class="p">):</span>
<span class="lineno special"> 10</span>     <span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">hostpath</span><span class="p">,</span> <span class="n">view_name</span><span class="p">,</span> <span class="n">args</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">,</span> <span class="n">asvar</span><span class="p">):</span>
<span class="lineno"> 11</span>         <span class="bp">self</span><span class="o">.</span><span class="n">hostpath</span> <span class="o">=</span> <span class="n">hostpath</span>
<span class="lineno"> 12</span>         <span class="bp">self</span><span class="o">.</span><span class="n">view_name</span> <span class="o">=</span> <span class="n">view_name</span>
<span class="lineno"> 13</span>         <span class="bp">self</span><span class="o">.</span><span class="n">args</span> <span class="o">=</span> <span class="n">args</span>
<span class="lineno"> 14</span>         <span class="bp">self</span><span class="o">.</span><span class="n">kwargs</span> <span class="o">=</span> <span class="n">kwargs</span>
<span class="lineno"> 15</span>         <span class="bp">self</span><span class="o">.</span><span class="n">asvar</span> <span class="o">=</span> <span class="n">asvar</span>
<span class="lineno"> 16</span>         <span class="k">print</span> <span class="bp">self</span><span class="o">.</span><span class="n">view_name</span>
<span class="lineno"> 17</span> 
<span class="lineno"> 18</span>     <span class="k">def</span> <span class="nf">render</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">context</span><span class="p">):</span>
<span class="lineno"> 19</span>         <span class="k">from</span> <span class="nn">django.core.urlresolvers</span> <span class="k">import</span> <span class="n">reverse</span><span class="p">,</span> <span class="n">NoReverseMatch</span>
<span class="lineno special"> 20</span>         <span class="n">args</span> <span class="o">=</span> <span class="p">[</span><span class="n">arg</span><span class="o">.</span><span class="n">resolve</span><span class="p">(</span><span class="n">context</span><span class="p">)</span> <span class="k">for</span> <span class="n">arg</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">args</span><span class="p">]</span>
<span class="lineno"> 21</span>         <span class="n">kwargs</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">([(</span><span class="n">smart_str</span><span class="p">(</span><span class="n">k</span><span class="p">,</span><span class="s">&#39;ascii&#39;</span><span class="p">),</span> <span class="n">v</span><span class="o">.</span><span class="n">resolve</span><span class="p">(</span><span class="n">context</span><span class="p">))</span>
<span class="lineno"> 22</span>                        <span class="k">for</span> <span class="n">k</span><span class="p">,</span> <span class="n">v</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">kwargs</span><span class="o">.</span><span class="n">items</span><span class="p">()])</span>
<span class="lineno"> 23</span>         
<span class="lineno"> 24</span>         
<span class="lineno"> 25</span>         <span class="c"># Try to look up the URL twice: once given the view name, and again</span>
<span class="lineno"> 26</span>         <span class="c"># relative to what we guess is the &quot;main&quot; app. If they both fail, </span>
<span class="lineno"> 27</span>         <span class="c"># re-raise the NoReverseMatch unless we&#39;re using the </span>
<span class="lineno"> 28</span>         <span class="c"># {% hosturl ... as var %} construct in which cause return nothing.</span>
<span class="lineno"> 29</span>         <span class="n">url</span> <span class="o">=</span> <span class="s">&#39;&#39;</span>
<span class="lineno special"> 30</span>         <span class="k">try</span><span class="p">:</span>
<span class="lineno"> 31</span>             <span class="n">url</span> <span class="o">=</span> <span class="n">reverse</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">view_name</span><span class="p">,</span> <span class="n">args</span><span class="o">=</span><span class="n">args</span><span class="p">,</span> <span class="n">kwargs</span><span class="o">=</span><span class="n">kwargs</span><span class="p">)</span>
<span class="lineno"> 32</span>         <span class="k">except</span> <span class="n">NoReverseMatch</span><span class="p">:</span>
<span class="lineno"> 33</span>             <span class="n">project_name</span> <span class="o">=</span> <span class="n">settings</span><span class="o">.</span><span class="n">SETTINGS_MODULE</span><span class="o">.</span><span class="kp">split</span><span class="p">(</span><span class="s">&#39;.&#39;</span><span class="p">)[</span><span class="mf">0</span><span class="p">]</span>
<span class="lineno"> 34</span>             <span class="k">try</span><span class="p">:</span>
<span class="lineno"> 35</span>                 <span class="n">url</span> <span class="o">=</span> <span class="n">reverse</span><span class="p">(</span><span class="n">project_name</span> <span class="o">+</span> <span class="s">&#39;.&#39;</span> <span class="o">+</span> <span class="bp">self</span><span class="o">.</span><span class="n">view_name</span><span class="p">,</span>
<span class="lineno"> 36</span>                               <span class="n">args</span><span class="o">=</span><span class="n">args</span><span class="p">,</span> <span class="n">kwargs</span><span class="o">=</span><span class="n">kwargs</span><span class="p">)</span>
<span class="lineno"> 37</span>             <span class="k">except</span> <span class="n">NoReverseMatch</span><span class="p">:</span>
<span class="lineno"> 38</span>                 <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">asvar</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span>
<span class="lineno"> 39</span>                     <span class="k">raise</span>
<span class="lineno special"> 40</span>                     
<span class="lineno"> 41</span>         <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">asvar</span><span class="p">:</span>
<span class="lineno"> 42</span>             <span class="n">context</span><span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">asvar</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">hostpath</span> <span class="o">+</span> <span class="n">url</span>
<span class="lineno"> 43</span>             <span class="k">return</span> <span class="s">&#39;&#39;</span>
<span class="lineno"> 44</span>         <span class="k">else</span><span class="p">:</span>
<span class="lineno"> 45</span>             <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">hostpath</span> <span class="o">+</span> <span class="n">url</span>
<span class="lineno"> 46</span> 
<span class="lineno"> 47</span> <span class="k">def</span> <span class="nf">hosturl</span><span class="p">(</span><span class="n">parser</span><span class="p">,</span> <span class="n">token</span><span class="p">):</span>
<span class="lineno"> 48</span>     <span class="sd">&quot;&quot;&quot;</span>
<span class="lineno"> 49</span> <span class="sd">    Returns an absolute URL matching given view with its parameters.</span>
<span class="lineno special"> 50</span> 
<span class="lineno"> 51</span> <span class="sd">    This is a way to define links that aren&#39;t tied to a particular URL</span>
<span class="lineno"> 52</span> <span class="sd">    configuration::</span>
<span class="lineno"> 53</span> 
<span class="lineno"> 54</span> <span class="sd">        {% hosturl hostpath path.to.some_view arg1,arg2,name1=value1 %}</span>
<span class="lineno"> 55</span> 
<span class="lineno"> 56</span> <span class="sd">    The first argument is a path to a view. It can be an absolute python path</span>
<span class="lineno"> 57</span> <span class="sd">    or just ``app_name.view_name`` without the project name if the view is</span>
<span class="lineno"> 58</span> <span class="sd">    located inside the project.  Other arguments are comma-separated values</span>
<span class="lineno"> 59</span> <span class="sd">    that will be filled in place of positional and keyword arguments in the</span>
<span class="lineno special"> 60</span> <span class="sd">    URL. All arguments for the URL should be present.</span>
<span class="lineno"> 61</span> 
<span class="lineno"> 62</span> <span class="sd">    For example if you have a view ``app_name.client`` taking client&#39;s id and</span>
<span class="lineno"> 63</span> <span class="sd">    the corresponding line in a URLconf looks like this::</span>
<span class="lineno"> 64</span> 
<span class="lineno"> 65</span> <span class="sd">        (&#39;^client/(\d+)/$&#39;, &#39;app_name.client&#39;)</span>
<span class="lineno"> 66</span> 
<span class="lineno"> 67</span> <span class="sd">    and this app&#39;s URLconf is included into the project&#39;s URLconf under some</span>
<span class="lineno"> 68</span> <span class="sd">    path::</span>
<span class="lineno"> 69</span> 
<span class="lineno special"> 70</span> <span class="sd">        (&#39;^clients/&#39;, include(&#39;project_name.app_name.urls&#39;))</span>
<span class="lineno"> 71</span> 
<span class="lineno"> 72</span> <span class="sd">    then in a template you can create a link for a certain client like this::</span>
<span class="lineno"> 73</span> 
<span class="lineno"> 74</span> <span class="sd">        {% hosturl http://other_server/path/to app_name.client client.id %}</span>
<span class="lineno"> 75</span> 
<span class="lineno"> 76</span> <span class="sd">    The URL will look like ``http://other_server/path/to/clients/client/123/``.</span>
<span class="lineno"> 77</span> <span class="sd">    &quot;&quot;&quot;</span>
<span class="lineno"> 78</span>     <span class="n">bits</span> <span class="o">=</span> <span class="n">token</span><span class="o">.</span><span class="n">contents</span><span class="o">.</span><span class="kp">split</span><span class="p">(</span><span class="s">&#39; &#39;</span><span class="p">)</span>
<span class="lineno"> 79</span>     <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">bits</span><span class="p">)</span> <span class="o">&lt;</span> <span class="mf">3</span><span class="p">:</span>
<span class="lineno special"> 80</span>         <span class="k">raise</span> <span class="n">TemplateSyntaxError</span><span class="p">(</span><span class="s">&quot;&#39;</span><span class="si">%s</span><span class="s">&#39; takes at least two arguments&quot;</span>
<span class="lineno"> 81</span>                                   <span class="s">&quot; (hostpath and path to a view)&quot;</span> <span class="o">%</span> <span class="n">bits</span><span class="p">[</span><span class="mf">0</span><span class="p">])</span>
<span class="lineno"> 82</span>     <span class="n">hostpath</span> <span class="o">=</span> <span class="n">bits</span><span class="p">[</span><span class="mf">1</span><span class="p">]</span>
<span class="lineno"> 83</span>     <span class="n">viewname</span> <span class="o">=</span> <span class="n">bits</span><span class="p">[</span><span class="mf">2</span><span class="p">]</span>
<span class="lineno"> 84</span>     <span class="n">args</span> <span class="o">=</span> <span class="p">[]</span>
<span class="lineno"> 85</span>     <span class="n">kwargs</span> <span class="o">=</span> <span class="p">{}</span>
<span class="lineno"> 86</span>     <span class="n">asvar</span> <span class="o">=</span> <span class="bp">None</span>
<span class="lineno"> 87</span>         
<span class="lineno"> 88</span>     <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">bits</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mf">3</span><span class="p">:</span>
<span class="lineno"> 89</span>         <span class="n">bits</span> <span class="o">=</span> <span class="nb">iter</span><span class="p">(</span><span class="n">bits</span><span class="p">[</span><span class="mf">3</span><span class="p">:])</span>
<span class="lineno special"> 90</span>         <span class="k">for</span> <span class="n">bit</span> <span class="ow">in</span> <span class="n">bits</span><span class="p">:</span>
<span class="lineno"> 91</span>             <span class="k">if</span> <span class="n">bit</span> <span class="o">==</span> <span class="s">&#39;as&#39;</span><span class="p">:</span>
<span class="lineno"> 92</span>                 <span class="n">asvar</span> <span class="o">=</span> <span class="n">bits</span><span class="o">.</span><span class="n">next</span><span class="p">()</span>
<span class="lineno"> 93</span>                 <span class="k">break</span>
<span class="lineno"> 94</span>             <span class="k">else</span><span class="p">:</span>
<span class="lineno"> 95</span>                 <span class="k">for</span> <span class="n">arg</span> <span class="ow">in</span> <span class="n">bit</span><span class="o">.</span><span class="kp">split</span><span class="p">(</span><span class="s">&quot;,&quot;</span><span class="p">):</span>
<span class="lineno"> 96</span>                     <span class="k">if</span> <span class="s">&#39;=&#39;</span> <span class="ow">in</span> <span class="n">arg</span><span class="p">:</span>
<span class="lineno"> 97</span>                         <span class="n">k</span><span class="p">,</span> <span class="n">v</span> <span class="o">=</span> <span class="n">arg</span><span class="o">.</span><span class="kp">split</span><span class="p">(</span><span class="s">&#39;=&#39;</span><span class="p">,</span> <span class="mf">1</span><span class="p">)</span>
<span class="lineno"> 98</span>                         <span class="n">k</span> <span class="o">=</span> <span class="n">k</span><span class="o">.</span><span class="n">strip</span><span class="p">()</span>
<span class="lineno"> 99</span>                         <span class="n">kwargs</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">parser</span><span class="o">.</span><span class="n">compile_filter</span><span class="p">(</span><span class="n">v</span><span class="p">)</span>
<span class="lineno special">100</span>                     <span class="k">elif</span> <span class="n">arg</span><span class="p">:</span>
<span class="lineno">101</span>                         <span class="n">args</span><span class="o">.</span><span class="kp">append</span><span class="p">(</span><span class="n">parser</span><span class="o">.</span><span class="n">compile_filter</span><span class="p">(</span><span class="n">arg</span><span class="p">))</span>
<span class="lineno">102</span>     <span class="k">return</span> <span class="n">HostURLNode</span><span class="p">(</span><span class="n">hostpath</span><span class="p">,</span> <span class="n">viewname</span><span class="p">,</span> <span class="n">args</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">,</span> <span class="n">asvar</span><span class="p">)</span>
<span class="lineno">103</span> <span class="n">hosturl</span> <span class="o">=</span> <span class="n">register</span><span class="o">.</span><span class="n">tag</span><span class="p">(</span><span class="n">hosturl</span><span class="p">)</span>
</pre></div>

        
    </div></td>
  </tr>
</table>

      </div>

      <div id="footer">
        &copy; 2002-2009 Dennis Kaarsemaker
      </div>

    </div>
  </body>
</html>
