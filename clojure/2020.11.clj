(use '[io :rename {read-all-lines yummy, printI printI}])
(use '[cartesian :only (grid, addvec, neighbors, dirs)])
(use '[util :only (untilrepeat)])

(def inp
  (->> (yummy)
       (map (partial map #(if (= \L %) 1 0)))
       (grid)
       ))

; can this be generalized? is it worthwhle to do so?
(defn sight [m pt]
  (map (fn [dir]
    (->> pt
         (iterate (partial addvec dir))
         (next)
         (take-while #(contains? m %))
         (drop-while #(= 0 (get m %)))
         (first)
         ))
    dirs
    ))

; since these will never change, let's memoize it
(def bysight (memoize (partial sight inp)))

; could perhaps generalize this with a neighbors function and an update function
(defn step [seatgrid]
  (->> seatgrid
       (reduce-kv
         (fn [m k v]
           (->> (neighbors k)
                (filter #(= 2 (get seatgrid %)))
                (count)
                (#(if (and (= 1 v) (= 0 %))
                    2
                    (if (and (= 2 v) (> % 3))
                      1
                      v
                      )))
                (assoc m k)
                ))
         {})
       ))

(defn step2 [seatgrid]
  (->> seatgrid
       (reduce-kv
         (fn [m k v]
           (->> (bysight k)
                (filter #(= 2 (get seatgrid %)))
                (count)
                (#(if (and (= 1 v) (= 0 %))
                    2
                    (if (and (= 2 v) (> % 4))
                      1
                      v
                      )))
                (assoc m k)
                ))
         {})
       ))

;(->> inp
;     (vector)
;     ((juxt
;        (partial untilrepeat step)
;        (partial untilrepeat step2)
;        ))
;     (map
;       #(->> %
;             (vals)
;             (filter (partial = 2))
;             (count)
;             ; (println) ; TODO: why doesn't this print?
;             ))
;     ; (map println) ; TODO: why doesn't this work?
;     ; TODO: wtf?
;     ((juxt
;        #(println (first %))
;        #(println (second %))
;        ))
;     )

(->> inp
     (vector)
     ((juxt
        ; this is less DRY, but also less ugly.
        ; because, for some reason, (map println) doesn't print anything
        ; perhaps because the sequences are lazy and thus aren't "realized"?
        ; but shouldn't (map println) force realization?
        #(->> %
              (untilrepeat step)
              (vals)
              (filter (partial = 2))
              (count)
              (println)
              )
        #(->> %
              (untilrepeat step2)
              (vals)
              (filter (partial = 2))
              (count)
              (println)
              )
        ))
     )
