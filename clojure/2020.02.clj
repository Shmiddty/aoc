(use '[io :rename {read-all-lines yummy}])

(def inp
  (->> (yummy)
       (map
         #(->> %
               (re-matches #"(\d+)-(\d+) ([a-z]+): ([a-z]+)")
               (rest) ; the first value is the string itself, which is not useful
               (map read-string) ; not sure why this is necessary,
               ; but it gives each value a type that we can cast to the types we actually want:
               ((fn [[a b c d]] [(int a) (int b) (first (str c)) (str d)]))
               ))
       ))

; Part 1
(->> inp
     (filter
       (fn [[mn mx ch pw]]
         (->> pw
              (filter #(= ch %))
              (count)
              (#(and (>= % mn) (<= % mx)))
              )))
     (count)
     (println) ; 393
     )

; Part 2
(->> inp
     (filter
       (fn [[o0 o1 ch pw]]
         (->> [o0 o1]
              (map #(- % 1)) ; change ordinals to indices
              (map #(nth pw %))
              (filter #(= ch %))
              (count)
              (= 1)
              )))
     (count)
     (println) ; 690
     )
