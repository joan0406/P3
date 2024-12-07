PAV - P3: estimación de pitch
=============================

Esta práctica se distribuye a través del repositorio GitHub [Práctica 3](https://github.com/albino-pav/P3).
Siga las instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para realizar un `fork` de la
misma y distribuir copias locales (*clones*) del mismo a los distintos integrantes del grupo de prácticas.

Recuerde realizar el *pull request* al repositorio original una vez completada la práctica.

Ejercicios básicos
------------------
- Tareas TODO:
    ![TODO.html](img/1todo)
    ![get_pitch](img/get_pitch)
    ![run_get_pitch](img/run_get_pitch.png)

- Complete el código de los ficheros necesarios para realizar la estimación de pitch usando el programa
  `get_pitch`.

   * Complete el cálculo de la autocorrelación e inserte a continuación el código correspondiente.
    
   **Codigo Autocorrelación**
    for (unsigned int l = 0; l < r.size(); ++l) {
      
      void PitchAnalyzer::autocorrelation(const vector<float> &x, vector<float> &r) const {
      /// \TODO Compute the autocorrelation r[l]
      /// \FET autocorrelacio calculada
      r[l] = 0;
      for(unsigned int n=l; n< x.size(); n++){
        r[l]+= x[n-l]*x[n];
      }
      r[l]=r[l]/x.size();
      
    }

    if (r[0] == 0.0F) //to avoid log() and divide zero 
      r[0] = 1e-10; 
    }


   * Inserte una gŕafica donde, en un *subplot*, se vea con claridad la señal temporal de un segmento de
     unos 30 ms de un fonema sonoro y su periodo de pitch; y, en otro *subplot*, se vea con claridad la
	 autocorrelación de la señal y la posición del primer máximo secundario.

   **Gráfica de la señal temporal de un fonema sonoro de 30ms y su autocorrelación con el primer máximo secundario y el periodo de pitch**

    ![Señal Temporal y Autocorrelación](img/autocorrelation_with_second_peak_corrected.png)

	 NOTA: es más que probable que tenga que usar Python, Octave/MATLAB u otro programa semejante para
	 hacerlo. Se valorará la utilización de la biblioteca matplotlib de Python.

   * Determine el mejor candidato para el periodo de pitch localizando el primer máximo secundario de la
     autocorrelación. Inserte a continuación el código correspondiente.
    
   **Codigo primer máximo secundario de la autocorrelación después del origen**

      vector<float>::const_iterator iR = r.begin(), iRMax = iR;

      float rMax= r[npitch_min];
      unsigned int  lag = npitch_min;
      for(unsigned int l= npitch_min; l<npitch_max; l++){
      if(r[l]>rMax){
        lag = l;
        rMax = r[l];
      }
    }

   * Implemente la regla de decisión sonoro o sordo e inserte el código correspondiente.
   
   **Codigo regla de decisión sordo o sonoro segun el llindar**
    
    bool PitchAnalyzer::unvoiced(float pot, float r1norm, float rmaxnorm) const {
    
      if(rmaxnorm<this->llindar_rmax){
        return true; //sordo
      }
        return false; //sonoro
    }

   
   * Puede serle útil seguir las instrucciones contenidas en el documento adjunto `código.pdf`.

- Una vez completados los puntos anteriores, dispondrá de una primera versión del estimador de pitch. El 
  resto del trabajo consiste, básicamente, en obtener las mejores prestaciones posibles con él.

  * Utilice el programa `wavesurfer` para analizar las condiciones apropiadas para determinar si un
    segmento es sonoro o sordo. 
	
	  - Inserte una gráfica con la estimación de pitch incorporada a `wavesurfer` y, junto a ella, los 
	    principales candidatos para determinar la sonoridad de la voz: el nivel de potencia de la señal
		(r[0]), la autocorrelación normalizada de uno (r1norm = r[1] / r[0]) y el valor de la
		autocorrelación en su máximo secundario (rmaxnorm = r[lag] / r[0]).

		Puede considerar, también, la conveniencia de usar la tasa de cruces por cero.

	    Recuerde configurar los paneles de datos para que el desplazamiento de ventana sea el adecuado, que
		en esta práctica es de 15 ms.

      - Use el estimador de pitch implementado en el programa `wavesurfer` en una señal de prueba y compare
	    su resultado con el obtenido por la mejor versión de su propio sistema.  Inserte una gráfica
		ilustrativa del resultado de ambos estimadores.

    **Gráfica wavesurfer indicando los principales candidatos para determinar sonoridad**

    ![Wavesurfer](img/wavesurfer.png)

    En la primera podemos ver el pitch contourn, luego vemos la gráfica de power plot y por último las gráficas de r1norm y rmaxnorm respectivamente. Hemos creado un script python llamado procesar_audio que genera los .txt con la información de las anteriores gráficas.
     
		Aunque puede usar el propio Wavesurfer para obtener la representación, se valorará
	 	el uso de alternativas de mayor calidad (particularmente Python).
  
  * Optimice los parámetros de su sistema de estimación de pitch e inserte una tabla con las tasas de error
    y el *score* TOTAL proporcionados por `pitch_evaluate` en la evaluación de la base de datos 
	`pitch_db/train`..
   
   **Comparación del Score total original vs ampliación hecha**

   ![run_get_pitch_sinmejoras](img/run_get_pitch_sinmejoras.png)
   ![run_get_pitch_conmejoras](img/run_get_pitch_conmejoras.png)


Ejercicios de ampliación
------------------------

- Usando la librería `docopt_cpp`, modifique el fichero `get_pitch.cpp` para incorporar los parámetros del
  estimador a los argumentos de la línea de comandos.
  
  Esta técnica le resultará especialmente útil para optimizar los parámetros del estimador. Recuerde que
  una parte importante de la evaluación recaerá en el resultado obtenido en la estimación de pitch en la
  base de datos.

  * Inserte un *pantallazo* en el que se vea el mensaje de ayuda del programa y un ejemplo de utilización
    con los argumentos añadidos.
    
    ![Mensaje de ayuda](img/ayudas.png)

- Implemente las técnicas que considere oportunas para optimizar las prestaciones del sistema de estimación
  de pitch.

  Entre las posibles mejoras, puede escoger una o más de las siguientes:

  * Técnicas de preprocesado: filtrado paso bajo, diezmado, *center clipping*, etc.
  
  **Central Clipping**
  float th_clipping = 0.004;
    for(int i = 0; i < (int)x.size(); i++) {
     if(abs(x[i]) < th_clipping) {
     x[i] = 0.0F;
    }
  }

Con un central clipping y probando diferentes tresholds hemos conseguido subir el score final a 89.00%

  * Técnicas de postprocesado: filtro de mediana, *dynamic time warping*, etc.
  
  **Filtro de Mediana**
  float L = 1;
  vector<float> med(L);

  for(int i = (L-1)/2; i < f0.size() - (L-1)/2; i++){
    for(int j = 0; j < L; j++){
      med[j] = f0[i+j-((L-1)/2)];
    }
    sort(med.begin(), med.end());

    f0[i] = med[(L-1)/2];
  }
  
  Hemos visto que  al implementar el filtro de mediana no mejoramos el score final y por tanto hemos dejado en L=1 que no hace nada.

  * Métodos alternativos a la autocorrelación: procesado cepstral, *average magnitude difference function*
    (AMDF), etc.
  * Optimización **demostrable** de los parámetros que gobiernan el estimador, en concreto, de los que
    gobiernan la decisión sonoro/sordo.
  * Cualquier otra técnica que se le pueda ocurrir o encuentre en la literatura.

  Encontrará más información acerca de estas técnicas en las [Transparencias del Curso](https://atenea.upc.edu/pluginfile.php/2908770/mod_resource/content/3/2b_PS%20Techniques.pdf)
  y en [Spoken Language Processing](https://discovery.upc.edu/iii/encore/record/C__Rb1233593?lang=cat).
  También encontrará más información en los anexos del enunciado de esta práctica.

  Incluya, a continuación, una explicación de las técnicas incorporadas al estimador. Se valorará la
  inclusión de gráficas, tablas, código o cualquier otra cosa que ayude a comprender el trabajo realizado.

  También se valorará la realización de un estudio de los parámetros involucrados. Por ejemplo, si se opta
  por implementar el filtro de mediana, se valorará el análisis de los resultados obtenidos en función de
  la longitud del filtro.
   

Evaluación *ciega* del estimador
-------------------------------

Antes de realizar el *pull request* debe asegurarse de que su repositorio contiene los ficheros necesarios
para compilar los programas correctamente ejecutando `make release`.

Con los ejecutables construidos de esta manera, los profesores de la asignatura procederán a evaluar el
estimador con la parte de test de la base de datos (desconocida para los alumnos). Una parte importante de
la nota de la práctica recaerá en el resultado de esta evaluación.
