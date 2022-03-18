(use '[io :rename {read-all-lines yummy, printI printI}])
(use '[clojure.string :only (split)])
(use '[enum :only (enumerate)])

(def inp
  (->> (yummy)
       ((fn [[a b]] [
          (read-string a)
          (split b #",")
          ]))
       ))

; so unpretty
(->> inp
     ((fn [[a B]]
        (->> B
             (filter #(not= "x" %))
             (map read-string)
             (map
               (fn [b]
                 (->> (iterate (partial + b) 0)
                      (drop-while (partial > a))
                      (first)
                      (vector b)
                 )))
             (apply min-key second)
             ((fn [[b t]] (* b (- t a))))
          )
        ))
     (println)
     )

; maybe this is actually a least common multiple problem, kinda.
; so is it better to iterate the busses like I was doing originally?
(->> inp
     (second)
     (enumerate)
     (filter #(not= "x" (second %)))
     (map (fn [[i d]] [i (read-string d)])) ; I should maybe make a function for this.
     ;(map (fn [[i d]] (map #(- % i) (iterate (partial + d) 0))))
     ((fn [ls]
        (->> ls
             (map (fn [[i d]] #(= 0 (mod (+ i %) d))))
             (apply every-pred)
             ; let's try to step lively
             ; looks like this is still too slow.
             (#(filter
                 %
                 (map
                   (partial + (* -1 (first (apply max-key second ls))))
                   (iterate (partial + (apply max (map second ls))) 0)
                   )))
             ; this is all pretty icky, huh?
             ; guess it was all a fluke, eh?
             ; guess my life has no value, right?
             (first)
             (printI)
             )))
     )
