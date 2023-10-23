Sequence Data
================

#### Section 5.3 - Sequence Data

``` r
library(dplyr)
```

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

``` r
library(TraMineR)
```

    ## 
    ## TraMineR stable version 2.2-6 (Built: 2023-02-06)

    ## Website: http://traminer.unige.ch

    ## Please type 'citation("TraMineR")' for citation information.

``` r
convos <- read.csv("convos.csv", sep = ",", header = FALSE)
convos <- convos[-1, ]
```

``` r
seq <- seqdef(convos)
```

    ##  [>] 8 distinct states appear in the data:

    ##      1 =

    ##      2 = aff.nor

    ##      3 = aff.off

    ##      4 = chunk

    ##      5 = end

    ##      6 = phone

    ##      7 = piss.off

    ##      8 = questn

    ##  [>] state coding:

    ##        [alphabet]  [label]  [long label]

    ##      1

    ##      2  aff.nor     aff.nor  aff.nor

    ##      3  aff.off     aff.off  aff.off

    ##      4  chunk       chunk    chunk

    ##      5  end         end      end

    ##      6  phone       phone    phone

    ##      7  piss.off    piss.off piss.off

    ##      8  questn      questn   questn

    ##  [>] 25036 sequences in the data set

    ##  [>] min/max sequence length: 6/6

``` r
seqplot(seq, type = 'i', legend.prop = c(0.25))
```

![](sequence_data_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

``` r
seqplot(seq, type = 'f', legend.prop = c(0.25))
```

![](sequence_data_files/figure-gfm/unnamed-chunk-3-2.png)<!-- -->

``` r
seqplot(seq, type = 'd', legend.prop = c(0.25))
```

![](sequence_data_files/figure-gfm/unnamed-chunk-3-3.png)<!-- -->

``` r
# DO NOT RUN, ONLY KNIT
seqplot(seq, type = 'I', sortv = 'from.start', legend.prop = c(0.25))
```

![](sequence_data_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->

``` r
seqtrate(seq)
```

    ##  [>] computing transition probabilities for states /aff.nor/aff.off/chunk/end/phone/piss.off/questn ...

    ##                    [-> ] [-> aff.nor] [-> aff.off] [-> chunk]  [-> end]
    ## [ ->]         1.00000000    0.0000000   0.00000000 0.00000000 0.0000000
    ## [aff.nor ->]  0.00000000    0.4620625   0.03671830 0.14692699 0.1041667
    ## [aff.off ->]  0.00000000    0.0000000   0.66666667 0.00000000 0.1840639
    ## [chunk ->]    0.00000000    0.1745110   0.01338980 0.43182093 0.1589837
    ## [end ->]      1.00000000    0.0000000   0.00000000 0.00000000 0.0000000
    ## [phone ->]    1.00000000    0.0000000   0.00000000 0.00000000 0.0000000
    ## [piss.off ->] 0.05276772    0.4211071   0.03362649 0.14019659 0.1169167
    ## [questn ->]   0.00000000    0.2783781   0.02206380 0.09131963 0.2548627
    ##                [-> phone] [-> piss.off] [-> questn]
    ## [ ->]         0.000000000   0.000000000   0.0000000
    ## [aff.nor ->]  0.035319851   0.022644148   0.1921615
    ## [aff.off ->]  0.008514664   0.140754757   0.0000000
    ## [chunk ->]    0.017463198   0.009114741   0.1947167
    ## [end ->]      0.000000000   0.000000000   0.0000000
    ## [phone ->]    0.000000000   0.000000000   0.0000000
    ## [piss.off ->] 0.038799793   0.022245215   0.1743404
    ## [questn ->]   0.027289442   0.013773749   0.3123125
