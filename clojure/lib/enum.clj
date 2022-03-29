(ns enum)

(defn make-hash-map [ls] (apply merge (map (partial apply hash-map) ls)))

; flatten by one level
(defn flat [ls]
  (apply conj [] ls))

; what's this called?
; [a + b for a in A for b in B]
;(defn krisskrosswillmakeyoujumpjump [A B] (mapcat (fn [a] (map (partial conj [a]) B)) A))
(defn cross [A B] (mapcat (fn [a] (map #(concat [a] [%]) B)) A))

(defn pairs [[head & tail]]
  (if (empty? tail)
    []
    (apply conj (map #(vector head %) tail) (pairs tail))))

(defn combinations [N ls]
  (if (or (< N 2) (empty? ls))
    (mapv vector ls)
    (concat
      (mapv (partial concat [(first ls)]) (combinations (- N 1) (rest ls)))
      (combinations N (rest ls))
      )
    ))

(defn has [v ls] (< 0 (count (filter (partial = v) ls))))

;(defn enumerate [ls] (zipmap (range (count ls)) ls))

; Found a more elegant implementation of enumerate
;https://stackoverflow.com/a/67029691
(defn enumerate [ls] (map-indexed vector ls))

(defn zip [a & more]
  (map-indexed
    (fn [i A] (concat [A] (map #(nth % i) more)))
    (take (apply min (count a) (map count more)) a)
    ))

(defn slice
  ([ls start]
   (if (> 0 start)
     (slice ls (+ start (count ls)))
     (drop start ls)
     ))
  ([ls start end]
   (if (> 0 end)
     (slice ls start (+ end (count ls)))
     (take (- end start) (slice ls start))
     ))
  ([ls start end step]
   (if (> step 0)
     (take-nth step (slice ls start end))
     ; (if (zero? step) infinitely recurs
     (slice (reverse ls) (- (count ls) end) (- (count ls) start) (- 0 step))
     ))
  )

