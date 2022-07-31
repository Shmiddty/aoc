(use '[clojure.string :only (split, join)])
(use '[io :rename {read-all yummy, printI dbg}])
(use '[enum :only (make-hash-map, zip, cross, slice)])
(use '[cartesian :only (enum2d, addvec, turn, mirror)])
(use '[util :only (fargo)])

(defn printgrid [grid] (println (join "\n" (map (partial apply str) grid))))

(defn fsecond [a] (first (second a)))
(defn sfsecond [a] (second (fsecond a)))
(defn sfirst [a] (second (first a)))
(defn fsfirst [a] (first (sfirst a)))

(defn rotate [tile]; 90 degrees clockwise
  (apply zip (reverse tile)))

(defn variants [tile]
  (concat
    (take 4 (iterate rotate tile))
    (take 4 (iterate rotate (reverse tile)))
    ))

; remove the border
(defn unwrap [tile] (map #(slice % 1 -1) (slice tile 1 -1)))

;  3
;2 a 0
;  1
(defn matches [a b]
  (cond
    (= (last a) (first b)) [0  1] ; a is above b
    (= (first a) (last b)) [0 -1] ; a is below b
    (= (last (apply zip a)) (first (apply zip b))) [ 1 0] ; a is left of b
    (= (first (apply zip a)) (last (apply zip b))) [-1 0] ; a is right of b
    :else false
    ))

(def inp
  (as-> (yummy) I
    (split I #"\n\n")
    (map #(split % #"\n") I)
    (map
      (juxt
        #(read-string (first (re-seq #"\d+" (first %))))
        #(variants (map vec (rest %)))
        )
      I
      )
    ))

(defn pgi [a] (do (printgrid a) (println "") a))

; [ [[idA tileA] [ [idB0 posB0 tileB0] .. [idBN posBN tileBN]]] .. ]
(def matching
  (sort-by #(count (second %))
  (map
    (fn [[idA tilesA]] [
      [idA (first tilesA)]
      (filter
        identity
        (map
          (fn [[idB tilesB]]
            (first
              (filter
                second
                (map #(vector idB (matches (first tilesA) %) %) tilesB)
                ))
            )
          (filter #(not= idA (first %)) inp)
          )
        )
      ])
    inp
    )))

; for part 1, I need only to find the four tiles that match with only two tiles.
; but surely I'd need to solve the whole puzzle for part 2, right?

(def corners (take 4 matching))
;(filter #(= 2 (count (second %))) matching))

; Part 1
(->> corners
     (map ffirst)
     (reduce *)
     (println)
     )

(defn ptvariants [pt]
  (concat
    (take 4 (iterate turn pt))
    (take 4 (iterate turn (mirror pt))) ; this is wrong?
    ))

; this part appears to be wrong
; DONE: fix this
; Some tiles are flipped. why? 
; my mirror function only mirrored the direction vector over the x axis,
; so if the vector were, for example, [1 0], it would remain unchanged.
; Thus the ptvariants function would have values repeated for some direction vectors.
; still not quite right.
(defn place [tileA [posA tileBA] rposB tileB]
  (->> (zip (variants tileBA) (ptvariants rposB) (variants tileB))
       (drop-while #(not= tileA (first %)))
       (first)
       (#(do (printgrid tileA) (println (second %)) (printgrid (nth % 2)) (println "\n") %))
       ;(#(do
       ;    (printgrid (first %)) (println "")
       ;    ;(printgrid (nth % 2)) (println "")
       ;    (printgrid (rotate (nth % 2))) (println "")
       ;    %))
       (rest)
       (apply (fargo (partial addvec posA) identity))
       ;((fn [[pos tile]] [(addvec posA pos) tile]))
      ))

(defn solve [[[[id0 tile0] matches0] & more]]
  (loop [solved {id0 [[0 0] tile0]}
         [[idA tileA] matches] [[id0 tile0] matches0]
         unsolved more]
    (if (empty? unsolved)
      (vals solved)
      (if (contains? solved idA)
        (recur
          (apply assoc solved
            (mapcat
              (fn [[idB pos tileB]] [idB (place tileA (get solved idA) pos tileB)])
              matches
              )
            )
          (first unsolved)
          (rest unsolved)
          )
        (recur solved (first unsolved) (concat (rest unsolved) [[[idA tileA] matches]]))
        ))))

(defn ptkey [[x y]] (+ (* y 1000) x))

; turn a flat collection into a square collection
(defn erect [coll] (partition (int (Math/sqrt (count coll))) coll))

(defn restitch [solved]
  (->> solved
       (sort-by #(ptkey (first %)))
       ;(#(do (mapv (fn [f] (do (println (first f)) (printgrid (second f)))) %) %))
       (map second)
       (map unwrap)
       (erect)
       (mapcat #(map (partial apply concat) (apply zip %)))
       ))

;;; This is clearly a picture of Nessy ;;;
;                                        ;
;                                        ;
;                            #           ;
;          #    ##    ##    ###          ;
;           #  #  #  #  #  #             ;
;                                        ;
;                                        ;
;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,;

(def nessies (map
  (fn [v] (filter #(= \# (second %)) (enum2d v)))
  (variants [
    "                  # "
    "#    ##    ##    ###"
    " #  #  #  #  #  #   "
  ])))

(defn
  findnessies
    [image]
       (->> image
             (enum2d)
                 (filter
       #(= \# (second %)))
         (make-hash-map)
        ((fn [imgmap]
             (mapcat
         (fn [nessy]
             (->> image
                 (enum2d)
                (filter
         (fn [[pt0 _]]
                    (every?
                 (fn [[ptN v]] (contains? imgmap
                                    (addvec pt0 ptN)))
                                               nessy
                                               )))
                ))
         nessies
      )))
    ))

(->> matching
     (dbg)
     (solve)
     (restitch)
     ;(#(do (printgrid %) %))
     ((juxt
       #(count (filter (partial = \#) (apply concat %)))
       #(* (count (first nessies)) (count (dbg (findnessies %))))
       ))
     (apply -)
     (println)
     )
; 1917 too high

